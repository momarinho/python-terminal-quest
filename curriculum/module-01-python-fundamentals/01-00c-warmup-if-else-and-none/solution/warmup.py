def classify_temp(celsius: int) -> str:
    """Return 'HOT' (>= 30), 'WARM' (15..29), or 'COLD' (< 15)."""
    if celsius >= 30:
        return "HOT"
    if celsius >= 15:
        return "WARM"
    return "COLD"


def normalize_retries(retries: int | None) -> int:
    """Return 3 only when retries is None; keep 0 as 0."""
    return 3 if retries is None else retries
