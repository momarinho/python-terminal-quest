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
        """Push an incident preserving FIFO order among equal priorities."""
        heapq.heappush(self._heap, (priority, self._seq, incident_id))
        self._seq += 1

    def peek_next(self) -> str | None:
        """Return the highest-urgency incident_id without removing it, or None if empty."""
        return self._heap[0][2] if self._heap else None

    def pop_next(self) -> str | None:
        """Remove and return the highest-urgency incident_id, or None if empty."""
        if not self._heap:
            return None
        _, _, incident_id = heapq.heappop(self._heap)
        return incident_id

    def drain_urgent(self, max_priority: int) -> list[str]:
        """Pop and return all incident_ids with priority <= max_priority in heap/FIFO order."""
        urgent: list[str] = []
        while self._heap and self._heap[0][0] <= max_priority:
            _, _, incident_id = heapq.heappop(self._heap)
            urgent.append(incident_id)
        return urgent
