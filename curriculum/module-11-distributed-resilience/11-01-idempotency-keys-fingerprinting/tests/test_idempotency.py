import pytest
from handler import IdempotentCommandHandler
from models import (
    CommandRequest,
    EmptyIdempotencyKeyError,
    IdempotencyConflictError,
)
from store import InMemoryIdempotencyStore


def test_identical_retry_replays_response_without_double_execution() -> None:
    calls = 0

    def charge(account_id: str, amount_cents: int, currency: str) -> str:
        nonlocal calls
        calls += 1
        return f"tx-{account_id}-{calls}"

    handler = IdempotentCommandHandler(InMemoryIdempotencyStore(), charge)
    req = CommandRequest(idempotency_key="key-100", account_id="acct-9", amount_cents=2500)

    first = handler.handle(req)
    retry = handler.handle(req)

    assert calls == 1
    assert first.status_code == 201
    assert first.replayed is False
    assert retry.replayed is True
    assert retry.transaction_id == first.transaction_id
    assert retry.debited_cents == 2500


def test_same_key_with_changed_payload_raises_conflict() -> None:
    handler = IdempotentCommandHandler(
        InMemoryIdempotencyStore(),
        lambda acct, amt, cur: f"tx-{acct}-{amt}-{cur}",
    )
    handler.handle(CommandRequest(idempotency_key="key-200", account_id="acct-1", amount_cents=1000))

    with pytest.raises(IdempotencyConflictError):
        handler.handle(
            CommandRequest(idempotency_key="key-200", account_id="acct-1", amount_cents=9999)
        )


def test_blank_idempotency_key_rejected() -> None:
    handler = IdempotentCommandHandler(
        InMemoryIdempotencyStore(),
        lambda acct, amt, cur: "tx-never",
    )
    with pytest.raises(EmptyIdempotencyKeyError):
        handler.handle(CommandRequest(idempotency_key="   ", account_id="acct-1", amount_cents=500))
