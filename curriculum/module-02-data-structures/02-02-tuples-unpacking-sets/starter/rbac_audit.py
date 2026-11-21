def split_route_record(record: tuple[str, ...]) -> tuple[str, str, tuple[str, ...]]:
    """Unpack (service, region, *endpoints) from a tuple record."""
    # TODO: validate length >= 2 and use starred unpacking
    return ("", "", ())


def audit_permission_drift(
    expected: list[str],
    actual: list[str],
) -> dict[str, list[str]]:
    """Return sorted 'missing', 'extra', and 'shared' permissions using set operations."""
    # TODO: use set difference and intersection
    return {"missing": [], "extra": [], "shared": []}


def dedupe_preserve_order(events: list[str]) -> list[str]:
    """Deduplicate event IDs in O(N) time while preserving first-seen order."""
    # TODO: maintain a seen set alongside output list
    return []
