from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import Literal, TypeVar

T = TypeVar("T")
CircuitState = Literal["CLOSED", "OPEN", "HALF_OPEN"]


class CircuitOpenError(RuntimeError):
    """Raised when calling an operation while its circuit breaker is OPEN."""


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 1,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be >= 1")
        if recovery_timeout < 0:
            raise ValueError("recovery_timeout must be >= 0")
        if half_open_max_calls < 1:
            raise ValueError("half_open_max_calls must be >= 1")
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max_calls = half_open_max_calls
        self._clock = clock
        self._lock = threading.Lock()
        self._state: CircuitState = "CLOSED"
        self._failure_count = 0
        self._opened_at = 0.0
        self._half_open_in_flight = 0

    @property
    def state(self) -> CircuitState:
        # TODO: Return current state (advancing OPEN -> HALF_OPEN if cooldown elapsed)
        raise NotImplementedError("TODO: implement state property")

    def call(self, fn: Callable[[], T]) -> T:
        # TODO:
        # 1. Check state under lock: fast-fail with CircuitOpenError when OPEN (unless cooled down to HALF_OPEN)
        # 2. Enforce half_open_max_calls cap when HALF_OPEN
        # 3. Execute fn() outside the lock
        # 4. Update state/counters under lock on success vs exception
        raise NotImplementedError("TODO: implement CircuitBreaker.call")
