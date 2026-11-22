import heapq
from collections import Counter, defaultdict


def top_error_codes(codes: list[str], k: int) -> list[tuple[str, int]]:
    """Return top-k (code, count) pairs ordered by count desc, then code asc."""
    _ = Counter
    return []


def group_alerts_by_service(alerts: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group (service, message) tuples into {service: [message, ...]} preserving order."""
    _ = defaultdict
    return {}


class IncidentPriorityQueue:
    """Min-heap priority queue (lower priority number = more urgent; FIFO tie-breaker)."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, str]] = []
        self._seq = 0

    def enqueue(self, priority: int, incident_id: str) -> None:
        """Push an incident preserving FIFO order among equal priorities."""
        _ = heapq

    def peek_next(self) -> str | None:
        """Return the highest-urgency incident_id without removing it, or None if empty."""
        return None

    def pop_next(self) -> str | None:
        """Remove and return the highest-urgency incident_id, or None if empty."""
        return None

    def drain_urgent(self, max_priority: int) -> list[str]:
        """Pop and return all incident_ids with priority <= max_priority in heap/FIFO order."""
        return []
