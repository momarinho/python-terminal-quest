def clean_label(raw: str) -> str:
    """Strip outer whitespace and lowercase a label string."""
    # Reveal: return raw.strip().lower()
    return raw


def parse_count(raw: str) -> int:
    """Strip whitespace and convert raw numeric text into an int."""
    # Reveal: return int(raw.strip())
    return 0


def is_enabled(raw: str) -> bool:
    """Return True if raw (case-insensitive) is 'true', '1', or 'yes'."""
    # Reveal: return raw.strip().lower() in {"true", "1", "yes"}
    return False
