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

    def _refresh_state_locked(self) -> CircuitState:
        if self._state == "OPEN" and (self._clock() - self._opened_at) >= self._recovery_timeout:
            self._state = "HALF_OPEN"
            self._half_open_in_flight = 0
        return self._state

    @property
    def state(self) -> CircuitState:
        with self._lock:
            return self._refresh_state_locked()

    def call(self, fn: Callable[[], T]) -> T:
        with self._lock:
            current = self._refresh_state_locked()
            if current == "OPEN":
                raise CircuitOpenError("Circuit breaker is OPEN; fast-failing call")
            is_probe = current == "HALF_OPEN"
            if is_probe:
                if self._half_open_in_flight >= self._half_open_max_calls:
                    raise CircuitOpenError("Circuit breaker HALF_OPEN probe slots exhausted")
                self._half_open_in_flight += 1

        try:
            result = fn()
        except BaseException:
            with self._lock:
                if is_probe:
                    self._half_open_in_flight = max(0, self._half_open_in_flight - 1)
                    self._state = "OPEN"
                    self._opened_at = self._clock()
                    self._failure_count = self._failure_threshold
                elif self._state == "CLOSED":
                    self._failure_count += 1
                    if self._failure_count >= self._failure_threshold:
                        self._state = "OPEN"
                        self._opened_at = self._clock()
            raise

        with self._lock:
            if is_probe:
                self._half_open_in_flight = max(0, self._half_open_in_flight - 1)
                self._state = "CLOSED"
                self._failure_count = 0
            elif self._state == "CLOSED":
                self._failure_count = 0
        return result
