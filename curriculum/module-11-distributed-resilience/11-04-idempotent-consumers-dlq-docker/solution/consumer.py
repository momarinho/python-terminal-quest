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
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return float(min(cap_seconds, base_seconds * (2**attempt)))


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
        if event_id in self.processed_ids:
            return "DUPLICATE"

        try:
            self._handler(event_id, payload)
        except Exception as exc:
            attempts = self._attempts.get(event_id, 0) + 1
            self._attempts[event_id] = attempts
            if attempts >= self._max_attempts:
                self.dlq.append(
                    DeadLetterRecord(
                        event_id=event_id,
                        payload=dict(payload),
                        attempts=attempts,
                        reason=str(exc),
                    )
                )
                return "DLQ"
            return "RETRY"

        self.processed_ids.add(event_id)
        return "PROCESSED"
