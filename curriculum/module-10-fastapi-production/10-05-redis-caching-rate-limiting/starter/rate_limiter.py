from __future__ import annotations

import time
from collections import deque
from collections.abc import Callable


class SlidingWindowRateLimiter:
    """Sliding-window limiter tracking exact timestamps per client key."""

    def __init__(
        self,
        limit: int,
        window_seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self._limit = limit
        self._window_seconds = window_seconds
        self._clock = clock
        self._events: dict[str, deque[float]] = {}

    def allow(self, client_key: str) -> tuple[bool, int]:
        """Return (allowed, retry_after_seconds)."""
        # TODO:
        # 1. Evict timestamps <= now - window_seconds from client deque
        # 2. If len >= limit, compute ceiling retry_after (>= 1) from oldest active timestamp
        # 3. Otherwise record now and return (True, 0)
        raise NotImplementedError("TODO: SlidingWindowRateLimiter.allow")
