import sqlite3

import pytest
from relay import OutboxRelay
from schema import init_outbox_schema
from service import InvoiceService


class FlakyBroker:
    def __init__(self, fail_until: int = 0) -> None:
        self.fail_until = fail_until
        self.calls = 0
        self.published: list[tuple[str, dict[str, object]]] = []

    def publish(self, event_type: str, payload: dict[str, object]) -> None:
        self.calls += 1
        if self.calls <= self.fail_until:
            raise ConnectionError("broker unreachable")
        self.published.append((event_type, payload))


def test_atomic_invoice_and_outbox_write_and_rollback() -> None:
    conn = sqlite3.connect(":memory:")
    init_outbox_schema(conn)
    svc = InvoiceService(conn)

    event_id = svc.issue_invoice("inv-1", "cust-9", 4500)
    assert event_id == "evt-inv-1"

    # Duplicate invoice fails and leaves zero extra rows
    with pytest.raises(sqlite3.IntegrityError):
        svc.issue_invoice("inv-1", "cust-9", 4500)

    inv_count = conn.execute("SELECT COUNT(*) FROM invoices").fetchone()[0]
    evt_count = conn.execute("SELECT COUNT(*) FROM outbox_events").fetchone()[0]
    assert inv_count == 1
    assert evt_count == 1


def test_relay_recovers_after_transient_broker_outage() -> None:
    conn = sqlite3.connect(":memory:")
    init_outbox_schema(conn)
    svc = InvoiceService(conn)
    svc.issue_invoice("inv-10", "cust-1", 1200)
    svc.issue_invoice("inv-11", "cust-2", 2400)

    broker = FlakyBroker(fail_until=1)
    relay = OutboxRelay(conn, broker)

    pub1, fail1 = relay.flush_pending()
    assert (pub1, fail1) == (1, 1)

    # First event stayed PENDING with error metadata; second published cleanly
    row10 = conn.execute("SELECT status, attempts, last_error FROM outbox_events WHERE id = 'evt-inv-10'").fetchone()
    assert row10["status"] == "PENDING"
    assert row10["attempts"] == 1
    assert "unreachable" in row10["last_error"]

    # Retry delivers inv-10 with zero duplicates of inv-11
    pub2, fail2 = relay.flush_pending()
    assert (pub2, fail2) == (1, 0)
    assert len(broker.published) == 2
