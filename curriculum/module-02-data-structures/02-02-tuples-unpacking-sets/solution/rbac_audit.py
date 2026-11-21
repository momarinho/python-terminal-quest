def split_route_record(record: tuple[str, ...]) -> tuple[str, str, tuple[str, ...]]:
    """Unpack (service, region, *endpoints) from a tuple record."""
    if len(record) < 2:
        raise ValueError("Route record must include at least service and region")
    service, region, *endpoints = record
    return service, region, tuple(endpoints)


def audit_permission_drift(
    expected: list[str],
    actual: list[str],
) -> dict[str, list[str]]:
    """Return sorted 'missing', 'extra', and 'shared' permissions using set operations."""
    exp_set = set(expected)
    act_set = set(actual)
    return {
        "missing": sorted(exp_set - act_set),
        "extra": sorted(act_set - exp_set),
        "shared": sorted(exp_set & act_set),
    }


def dedupe_preserve_order(events: list[str]) -> list[str]:
    """Deduplicate event IDs in O(N) time while preserving first-seen order."""
    seen: set[str] = set()
    unique: list[str] = []
    for event_id in events:
        if event_id not in seen:
            seen.add(event_id)
            unique.append(event_id)
    return unique
