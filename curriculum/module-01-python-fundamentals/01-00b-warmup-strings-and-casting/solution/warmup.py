def clean_label(raw: str) -> str:
    """Strip outer spaces and lowercase a label."""
    return raw.strip().lower()


def parse_count(raw: str) -> int:
    """Convert text like ' 42 ' into the integer 42."""
    return int(raw.strip())


def is_enabled(raw: str) -> bool:
    """Return True if raw is 'true', '1', or 'yes' (ignoring spaces/case)."""
    return raw.strip().lower() in {"true", "1", "yes"}
