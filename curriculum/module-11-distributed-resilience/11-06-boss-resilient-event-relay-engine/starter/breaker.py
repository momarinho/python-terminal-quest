from __future__ import annotations

import time
from collections.abc import Callable
from typing import Literal, TypeVar

T = TypeVar("T")
CircuitState = Literal["CLOSED", "OPEN", "HALF_OPEN"]


class CircuitOpenError(RuntimeError):
    """Raised when the circuit breaker is OPEN."""


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 2,
        recovery_timeout: float = 10.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._clock = clock
        self._state: CircuitState = "CLOSED"
        self._failure_count = 0
        self._opened_at = 0.0

    @property
    def state(self) -> CircuitState:
        # TODO: Handle OPEN -> HALF_OPEN cooldown transition
        raise NotImplementedError("TODO: state")

    def call(self, fn: Callable[[], T]) -> T:
        # TODO: Guard call with CLOSED -> OPEN -> HALF_OPEN state machine
        raise NotImplementedError("TODO: call")
