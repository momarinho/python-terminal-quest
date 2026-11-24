def clean_label(raw: str) -> str:
    """Strip outer whitespace and lowercase a label string."""
    return raw.strip().lower()


def parse_count(raw: str) -> int:
    """Strip whitespace and convert raw numeric text into an int."""
    return int(raw.strip())


def is_enabled(raw: str) -> bool:
    """Return True if raw (case-insensitive) is 'true', '1', or 'yes'."""
    return raw.strip().lower() in {"true", "1", "yes"}
