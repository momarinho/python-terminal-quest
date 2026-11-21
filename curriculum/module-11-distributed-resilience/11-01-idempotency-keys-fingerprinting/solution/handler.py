from __future__ import annotations

from collections.abc import Callable

from models import (
    CommandRequest,
    CommandResponse,
    EmptyIdempotencyKeyError,
    IdempotencyConflictError,
)
from store import IdempotencyRecord, InMemoryIdempotencyStore, compute_payload_sha256

PaymentExecutor = Callable[[str, int, str], str]


class IdempotentCommandHandler:
    def __init__(self, store: InMemoryIdempotencyStore, executor: PaymentExecutor) -> None:
        self._store = store
        self._executor = executor

    def handle(self, request: CommandRequest) -> CommandResponse:
        key = request.idempotency_key.strip()
        if not key:
            raise EmptyIdempotencyKeyError("Idempotency-Key must not be empty")

        payload_hash = compute_payload_sha256(
            request.account_id, request.amount_cents, request.currency
        )
        existing = self._store.get(key)
        if existing is not None:
            if existing.payload_hash != payload_hash:
                raise IdempotencyConflictError(
                    f"Idempotency key '{key}' already bound to a different payload"
                )
            return CommandResponse(
                status_code=existing.status_code,
                transaction_id=existing.transaction_id,
                debited_cents=existing.debited_cents,
                replayed=True,
            )

        tx_id = self._executor(request.account_id, request.amount_cents, request.currency)
        self._store.save(
            IdempotencyRecord(
                key=key,
                payload_hash=payload_hash,
                status_code=201,
                transaction_id=tx_id,
                debited_cents=request.amount_cents,
            )
        )
        return CommandResponse(
            status_code=201,
            transaction_id=tx_id,
            debited_cents=request.amount_cents,
            replayed=False,
        )
