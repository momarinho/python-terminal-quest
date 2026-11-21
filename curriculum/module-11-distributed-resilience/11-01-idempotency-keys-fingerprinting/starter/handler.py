from __future__ import annotations

from collections.abc import Callable

from models import (
    CommandRequest,
    CommandResponse,
)
from store import InMemoryIdempotencyStore

PaymentExecutor = Callable[[str, int, str], str]


class IdempotentCommandHandler:
    def __init__(self, store: InMemoryIdempotencyStore, executor: PaymentExecutor) -> None:
        self._store = store
        self._executor = executor

    def handle(self, request: CommandRequest) -> CommandResponse:
        # TODO:
        # 1. Validate request.idempotency_key.strip() is non-empty (else EmptyIdempotencyKeyError)
        # 2. Compute payload SHA-256 hash
        # 3. Check store: replay if hash matches, raise IdempotencyConflictError if hash differs
        # 4. Execute side effect once, save record (status_code=201), return CommandResponse(replayed=False)
        raise NotImplementedError("TODO: implement idempotent command handler")
