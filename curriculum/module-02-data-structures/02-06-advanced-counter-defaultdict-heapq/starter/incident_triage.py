import heapq
from collections import Counter, defaultdict


def top_error_codes(codes: list[str], k: int) -> list[tuple[str, int]]:
    """Return top-k (code, count) pairs ordered by count desc, then code asc."""
    # TODO: use Counter and deterministic tie-breaking
    _ = Counter
    return []


def group_alerts_by_service(alerts: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group (service, message) tuples into {service: [message, ...]} preserving order."""
    # TODO: use defaultdict(list)
    _ = defaultdict
    return {}


class IncidentPriorityQueue:
    """Min-heap priority queue (lower priority number = more urgent; FIFO tie-breaker)."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, str]] = []
        self._seq = 0

    def enqueue(self, priority: int, incident_id: str) -> None:
        # TODO: push (priority, seq, incident_id) with heapq.heappush
        _ = heapq

    def pop_next(self) -> str | None:
        # TODO: pop and return incident_id, or None if empty
        return None
