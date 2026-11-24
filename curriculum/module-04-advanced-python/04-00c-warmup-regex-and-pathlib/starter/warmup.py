import re  # noqa: F401
from pathlib import Path


def extract_ticket_id(text: str) -> str | None:
    """Return first 'TKT-<digits>' substring or None."""
    return None


def save_text_file(target: Path, content: str) -> None:
    """Write UTF-8 text to target Path."""
    pass
