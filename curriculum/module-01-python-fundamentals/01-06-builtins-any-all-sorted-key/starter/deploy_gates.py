def is_release_ready(checks: list[dict[str, object]]) -> bool:
    """Return True iff checks is non-empty and every check has passed=True."""
    # TODO: use bool(checks) and all(...)
    return False


def has_blocking_alert(alerts: list[dict[str, object]]) -> bool:
    """Return True if any alert has severity == 'critical' and acked == False."""
    # TODO: use any(...)
    return False


def rank_endpoints(endpoints: list[dict[str, object]]) -> list[str]:
    """Return endpoint paths ordered by highest error_rate, then highest p99_ms, then path asc."""
    # TODO: use sorted(..., key=...) without mutating input
    return []


def fastest_healthy_region(regions: list[dict[str, object]]) -> str:
    """Return the name of the healthy region with lowest latency_ms (tie-break name asc)."""
    # TODO: filter healthy regions, raise ValueError if none, use min(..., key=...)
    return ""
