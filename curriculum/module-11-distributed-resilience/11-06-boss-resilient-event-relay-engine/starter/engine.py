from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Protocol

from breaker import CircuitBreaker


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
        # TODO: Deduplicate via idempotency_keys + insert PENDING outbox_events row atomically
        raise NotImplementedError("TODO: submit_command")

    def dispatch_pending(self, limit: int = 50) -> DispatchReport:
        # TODO: Dispatch PENDING events through CircuitBreaker and route failures/DLQ
        raise NotImplementedError("TODO: dispatch_pending")
