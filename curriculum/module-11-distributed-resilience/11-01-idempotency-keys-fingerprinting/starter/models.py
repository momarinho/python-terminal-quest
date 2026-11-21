from __future__ import annotations

from dataclasses import dataclass


class EmptyIdempotencyKeyError(ValueError):
    """Raised when a mutating command omits a non-empty idempotency key."""


class IdempotencyConflictError(Exception):
    """Raised when the same idempotency key is reused with a different payload."""


@dataclass(frozen=True)
class CommandRequest:
    idempotency_key: str
    account_id: str
    amount_cents: int
    currency: str = "USD"


@dataclass(frozen=True)
class CommandResponse:
    status_code: int
    transaction_id: str
    debited_cents: int
    replayed: bool = False
