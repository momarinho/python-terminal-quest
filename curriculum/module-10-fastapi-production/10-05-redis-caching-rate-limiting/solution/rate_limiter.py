from __future__ import annotations

import math
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
        now = self._clock()
        bucket = self._events.setdefault(client_key, deque())
        cutoff = now - self._window_seconds
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()

        if len(bucket) >= self._limit:
            wait_seconds = (bucket[0] + self._window_seconds) - now
            return False, max(1, math.ceil(wait_seconds))

        bucket.append(now)
        return True, 0
