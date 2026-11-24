import re
from pathlib import Path


def extract_ticket_id(text: str) -> str | None:
    """Return first 'TKT-<digits>' substring or None."""
    match = re.search(r"TKT-\d+", text)
    return match.group(0) if match else None


def save_text_file(target: Path, content: str) -> None:
    """Write UTF-8 text to target Path."""
    target.write_text(content, encoding="utf-8")
