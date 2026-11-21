import sqlite3

import pytest
from breaker import CircuitBreaker
from engine import ResilientRelayEngine
from idempotency import IdempotencyConflictError
from outbox import init_engine_schema


class ControlledTransport:
    def __init__(self) -> None:
        self.fail_mode = False
        self.delivered: list[str] = []

    def send(self, event_id: str, event_type: str, payload: dict[str, object]) -> None:
        if payload.get("poison"):
            raise ValueError("poison payload")
        if self.fail_mode:
            raise ConnectionError("downstream unavailable")
        self.delivered.append(event_id)


def test_idempotent_submission_and_conflict() -> None:
    conn = sqlite3.connect(":memory:")
    init_engine_schema(conn)
    transport = ControlledTransport()
    engine = ResilientRelayEngine(conn, transport, CircuitBreaker())

    r1 = engine.submit_command("cmd-1", "OrderPaid", {"order_id": 10})
    r2 = engine.submit_command("cmd-1", "OrderPaid", {"order_id": 10})
    assert r1.event_id == r2.event_id
    assert r1.replayed is False
    assert r2.replayed is True

    with pytest.raises(IdempotencyConflictError):
        engine.submit_command("cmd-1", "OrderPaid", {"order_id": 99})

    assert conn.execute("SELECT COUNT(*) FROM outbox_events").fetchone()[0] == 1


def test_circuit_breaker_fast_fail_preserves_retry_budget_then_recovers() -> None:
    now = 0.0
    conn = sqlite3.connect(":memory:")
    init_engine_schema(conn)
    transport = ControlledTransport()
    transport.fail_mode = True
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=10.0, clock=lambda: now)
    engine = ResilientRelayEngine(conn, transport, breaker, max_attempts=3)

    for idx in range(3):
        engine.submit_command(f"k-{idx}", "PayoutSent", {"seq": idx})

    # First 2 fail and trip breaker OPEN; 3rd is skipped while OPEN without burning attempts
    rep1 = engine.dispatch_pending()
    assert (rep1.published, rep1.retried, rep1.skipped_circuit_open) == (0, 2, 1)
    assert breaker.state == "OPEN"

    k2_row = conn.execute("SELECT attempts, status FROM outbox_events WHERE id = 'evt-k-2'").fetchone()
    assert k2_row["attempts"] == 0
    assert k2_row["status"] == "PENDING"

    # Recover transport and advance virtual clock past cooldown
    transport.fail_mode = False
    now += 11.0
    rep2 = engine.dispatch_pending()
    assert rep2.published == 3
    assert breaker.state == "CLOSED"


def test_poison_message_moves_to_dead_letter_after_max_attempts() -> None:
    now = 0.0
    conn = sqlite3.connect(":memory:")
    init_engine_schema(conn)
    transport = ControlledTransport()
    breaker = CircuitBreaker(failure_threshold=10, recovery_timeout=5.0, clock=lambda: now)
    engine = ResilientRelayEngine(conn, transport, breaker, max_attempts=2)

    engine.submit_command("bad-1", "OrderPaid", {"poison": True})
    rep1 = engine.dispatch_pending()
    assert rep1.retried == 1
    assert rep1.dead_lettered == 0

    rep2 = engine.dispatch_pending()
    assert rep2.dead_lettered == 1

    row = conn.execute("SELECT status, attempts, last_error FROM outbox_events WHERE id = 'evt-bad-1'").fetchone()
    assert row["status"] == "DEAD_LETTER"
    assert row["attempts"] == 2
    assert "poison" in row["last_error"]
