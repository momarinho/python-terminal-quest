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

    def ingest(self, line: str) -> None:
        ts, service, status, _latency_ms = parse_log_line(line)
        is_error = 500 <= status < 600
        self._window.append((ts, service, is_error))
        self._requests[service] += 1
        if is_error:
            self._errors[service] += 1

        if ts > self._max_ts:
            self._max_ts = ts
        cutoff = self._max_ts - self.window_seconds

        while self._window and self._window[0][0] < cutoff:
            _, exp_svc, exp_err = self._window.popleft()
            self._requests[exp_svc] -= 1
            if self._requests[exp_svc] <= 0:
                del self._requests[exp_svc]
            if exp_err:
                self._errors[exp_svc] -= 1
                if self._errors[exp_svc] <= 0:
                    del self._errors[exp_svc]

    def active_count(self) -> int:
        return len(self._window)

    def top_failing_services(self, k: int) -> list[tuple[str, int]]:
        if k <= 0:
            return []
        heap_items = [(-cnt, svc) for svc, cnt in self._errors.items() if cnt > 0]
        top = heapq.nsmallest(k, heap_items)
        return [(svc, -neg_cnt) for neg_cnt, svc in top]

    def service_summary(self, service: str) -> dict[str, int]:
        return {
            "requests": self._requests.get(service, 0),
            "errors": self._errors.get(service, 0),
        }
