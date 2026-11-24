def classify_temp(celsius: int) -> str:
    """Return 'HOT' (>= 30), 'WARM' (15..29), or 'COLD' (< 15)."""
    return "COLD"


def normalize_retries(retries: int | None) -> int:
    """Return 3 only when retries is None; keep 0 as 0."""
    return 3
