from __future__ import annotations

import json
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
        rows = self._conn.execute(
            """
            SELECT id, event_type, payload_json
            FROM outbox_events
            WHERE status = 'PENDING'
            ORDER BY rowid ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        published = 0
        failed = 0
        for row in rows:
            event_id = str(row["id"])
            event_type = str(row["event_type"])
            payload = json.loads(str(row["payload_json"]))
            try:
                self._broker.publish(event_type, payload)
            except Exception as exc:
                failed += 1
                with self._conn:
                    self._conn.execute(
                        """
                        UPDATE outbox_events
                        SET attempts = attempts + 1, last_error = ?
                        WHERE id = ?
                        """,
                        (str(exc), event_id),
                    )
            else:
                published += 1
                with self._conn:
                    self._conn.execute(
                        """
                        UPDATE outbox_events
                        SET status = 'PUBLISHED', attempts = attempts + 1, last_error = ''
                        WHERE id = ?
                        """,
                        (event_id,),
                    )
        return published, failed
