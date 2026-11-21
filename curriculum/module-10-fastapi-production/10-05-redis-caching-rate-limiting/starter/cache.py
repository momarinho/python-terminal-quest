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
        # TODO: Return value if present and not expired (clock() >= expires_at evicts & returns None)
        raise NotImplementedError("TODO: InMemoryRedisCache.get")

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        # TODO: Store (value, self._clock() + ttl_seconds)
        raise NotImplementedError("TODO: InMemoryRedisCache.set")

    def delete(self, key: str) -> None:
        # TODO: Evict key if present
        raise NotImplementedError("TODO: InMemoryRedisCache.delete")
