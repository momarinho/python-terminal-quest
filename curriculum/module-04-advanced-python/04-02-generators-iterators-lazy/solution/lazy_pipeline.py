from collections.abc import Iterable, Iterator
from itertools import batched


def iter_non_empty_events(lines: Iterable[str]) -> Iterator[str]:
    """Lazily yield stripped non-blank, non-comment ('#') lines."""
    for raw in lines:
        cleaned = raw.strip()
        if cleaned and not cleaned.startswith("#"):
            yield cleaned


def iter_error_records(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Lazily parse 'LEVEL:message' lines from iter_non_empty_events and yield ERROR records."""
    for line in iter_non_empty_events(lines):
        if ":" not in line:
            continue
        level, message = line.split(":", 1)
        if level.strip().upper() == "ERROR":
            yield {"level": "ERROR", "message": message.strip()}


def batch_records[T](records: Iterable[T], size: int) -> Iterator[list[T]]:
    """Lazily yield lists of up to `size` records; raise ValueError immediately if size < 1."""
    if size < 1:
        raise ValueError(f"size must be >= 1, got {size}")
    return (list(chunk) for chunk in batched(records, size, strict=False))
