from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Protocol

from breaker import CircuitBreaker, CircuitOpenError
from idempotency import IdempotencyConflictError, fingerprint_command


class Transport(Protocol):
    def send(self, event_id: str, event_type: str, payload: dict[str, object]) -> None: ...


@dataclass(frozen=True)
class SubmitResult:
    event_id: str
    replayed: bool


@dataclass(frozen=True)
class DispatchReport:
    published: int
    retried: int
    dead_lettered: int
    skipped_circuit_open: int


class ResilientRelayEngine:
    def __init__(
        self,
        conn: sqlite3.Connection,
        transport: Transport,
        breaker: CircuitBreaker,
        max_attempts: int = 3,
    ) -> None:
        self._conn = conn
        self._transport = transport
        self._breaker = breaker
        self._max_attempts = max_attempts

    def submit_command(
        self,
        idempotency_key: str,
        event_type: str,
        payload: dict[str, object],
    ) -> SubmitResult:
        key = idempotency_key.strip()
        if not key:
            raise ValueError("idempotency_key must not be empty")
        payload_hash = fingerprint_command(event_type, payload)

        with self._conn:
            existing = self._conn.execute(
                "SELECT payload_hash, event_id FROM idempotency_keys WHERE key = ?",
                (key,),
            ).fetchone()
            if existing is not None:
                if str(existing["payload_hash"]) != payload_hash:
                    raise IdempotencyConflictError(
                        f"Idempotency key '{key}' already used for another payload"
                    )
                return SubmitResult(event_id=str(existing["event_id"]), replayed=True)

            event_id = f"evt-{key}"
            payload_json = json.dumps(payload, sort_keys=True)
            self._conn.execute(
                "INSERT INTO idempotency_keys (key, payload_hash, event_id) VALUES (?, ?, ?)",
                (key, payload_hash, event_id),
            )
            self._conn.execute(
                """
                INSERT INTO outbox_events (id, event_type, payload_json, status)
                VALUES (?, ?, ?, 'PENDING')
                """,
                (event_id, event_type, payload_json),
            )
        return SubmitResult(event_id=event_id, replayed=False)

    def dispatch_pending(self, limit: int = 50) -> DispatchReport:
        rows = self._conn.execute(
            """
            SELECT id, event_type, payload_json, attempts
            FROM outbox_events
            WHERE status = 'PENDING'
            ORDER BY rowid ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        published = 0
        retried = 0
        dead_lettered = 0
        skipped_open = 0

        for row in rows:
            event_id = str(row["id"])
            event_type = str(row["event_type"])
            payload = json.loads(str(row["payload_json"]))
            prev_attempts = int(row["attempts"])

            try:
                self._breaker.call(
                    lambda eid=event_id, etype=event_type, body=payload: self._transport.send(
                        eid, etype, body
                    )
                )
            except CircuitOpenError:
                skipped_open += 1
            except Exception as exc:
                next_attempts = prev_attempts + 1
                next_status = "DEAD_LETTER" if next_attempts >= self._max_attempts else "PENDING"
                if next_status == "DEAD_LETTER":
                    dead_lettered += 1
                else:
                    retried += 1
                with self._conn:
                    self._conn.execute(
                        """
                        UPDATE outbox_events
                        SET status = ?, attempts = ?, last_error = ?
                        WHERE id = ?
                        """,
                        (next_status, next_attempts, str(exc), event_id),
                    )
            else:
                published += 1
                with self._conn:
                    self._conn.execute(
                        """
                        UPDATE outbox_events
                        SET status = 'PUBLISHED', attempts = ?, last_error = ''
                        WHERE id = ?
                        """,
                        (prev_attempts + 1, event_id),
                    )

        return DispatchReport(
            published=published,
            retried=retried,
            dead_lettered=dead_lettered,
            skipped_circuit_open=skipped_open,
        )
