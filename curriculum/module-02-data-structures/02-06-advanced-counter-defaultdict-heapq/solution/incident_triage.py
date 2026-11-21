import heapq
from collections import Counter, defaultdict


def top_error_codes(codes: list[str], k: int) -> list[tuple[str, int]]:
    """Return top-k (code, count) pairs ordered by count desc, then code asc."""
    if k <= 0:
        return []
    counts = Counter(codes)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered[:k]


def group_alerts_by_service(alerts: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group (service, message) tuples into {service: [message, ...]} preserving order."""
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for service, message in alerts:
        grouped[service].append(message)
    return dict(grouped)


class IncidentPriorityQueue:
    """Min-heap priority queue (lower priority number = more urgent; FIFO tie-breaker)."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, str]] = []
        self._seq = 0

    def enqueue(self, priority: int, incident_id: str) -> None:
        heapq.heappush(self._heap, (priority, self._seq, incident_id))
        self._seq += 1

    def pop_next(self) -> str | None:
        if not self._heap:
            return None
        _, _, incident_id = heapq.heappop(self._heap)
        return incident_id
