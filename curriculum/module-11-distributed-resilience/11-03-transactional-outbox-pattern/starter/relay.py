from __future__ import annotations

import sqlite3
from typing import Protocol


class BrokerClient(Protocol):
    def publish(self, event_type: str, payload: dict[str, object]) -> None: ...


class OutboxRelay:
    def __init__(self, conn: sqlite3.Connection, broker: BrokerClient) -> None:
        self._conn = conn
        self._broker = broker

    def flush_pending(self, limit: int = 50) -> tuple[int, int]:
        """Publish PENDING events and return (published_count, failed_count)."""
        # TODO: Poll PENDING outbox rows, publish via self._broker.publish, mark PUBLISHED
        # on success or keep PENDING + increment attempts + record last_error on exception.
        raise NotImplementedError("TODO: implement outbox relay")
