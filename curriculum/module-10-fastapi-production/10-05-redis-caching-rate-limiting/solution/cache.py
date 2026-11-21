from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol


class CacheStore(Protocol):
    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str, ttl_seconds: int) -> None: ...
    def delete(self, key: str) -> None: ...


class InMemoryRedisCache:
    """Thread-safe/testable in-memory stand-in for Redis GET / SET EX / DEL."""

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._data: dict[str, tuple[str, float]] = {}

    def get(self, key: str) -> str | None:
        entry = self._data.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if self._clock() >= expires_at:
            self._data.pop(key, None)
            return None
        return value

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        self._data[key] = (value, self._clock() + max(0, ttl_seconds))

    def delete(self, key: str) -> None:
        self._data.pop(key, None)
