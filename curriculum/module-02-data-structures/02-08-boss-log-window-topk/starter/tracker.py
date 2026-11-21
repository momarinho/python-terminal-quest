import heapq
from collections import Counter, deque

from parser import parse_log_line


class SlidingWindowTopK:
    """Sliding-window log aggregator with O(1) deque eviction and heapq Top-K failing services."""

    def __init__(self, window_seconds: int) -> None:
        if window_seconds < 1:
            raise ValueError("window_seconds must be >= 1")
        self.window_seconds = window_seconds
        self._window: deque[tuple[int, str, bool]] = deque()
        self._requests: Counter[str] = Counter()
        self._errors: Counter[str] = Counter()
        self._max_ts = 0
        _ = (heapq, parse_log_line)

    def ingest(self, line: str) -> None:
        # TODO: parse line, append to deque, update counters, evict expired entries
        pass

    def active_count(self) -> int:
        return len(self._window)

    def top_failing_services(self, k: int) -> list[tuple[str, int]]:
        # TODO: return top-k (service, error_count) ordered by error_count desc, service asc
        return []

    def service_summary(self, service: str) -> dict[str, int]:
        return {
            "requests": self._requests.get(service, 0),
            "errors": self._errors.get(service, 0),
        }
