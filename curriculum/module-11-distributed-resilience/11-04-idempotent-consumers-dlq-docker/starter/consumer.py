from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

ConsumeOutcome = Literal["PROCESSED", "DUPLICATE", "RETRY", "DLQ"]


@dataclass(frozen=True)
class DeadLetterRecord:
    event_id: str
    payload: dict[str, object]
    attempts: int
    reason: str


def compute_backoff_seconds(
    attempt: int,
    base_seconds: float = 0.5,
    cap_seconds: float = 8.0,
) -> float:
    """Compute bounded exponential backoff min(cap, base * 2**attempt)."""
    # TODO: Validate attempt >= 0 and compute capped exponential delay
    raise NotImplementedError("TODO: compute_backoff_seconds")


class EventConsumer:
    def __init__(
        self,
        handler: Callable[[str, dict[str, object]], None],
        max_attempts: int = 3,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        self._handler = handler
        self._max_attempts = max_attempts
        self.processed_ids: set[str] = set()
        self._attempts: dict[str, int] = {}
        self.dlq: list[DeadLetterRecord] = []

    def consume(self, event_id: str, payload: dict[str, object]) -> ConsumeOutcome:
        """Process an event idempotently, retrying transiently or routing poison events to DLQ."""
        # TODO:
        # 1. Return "DUPLICATE" if event_id already processed
        # 2. Invoke handler; on success mark processed_ids and return "PROCESSED"
        # 3. On error, increment attempt count; if >= max_attempts append DeadLetterRecord and return "DLQ", else "RETRY"
        raise NotImplementedError("TODO: implement EventConsumer.consume")
