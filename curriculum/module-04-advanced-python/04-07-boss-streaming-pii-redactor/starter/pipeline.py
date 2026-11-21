from collections.abc import Iterable, Iterator
from pathlib import Path

from patterns import redact_line


def iter_redacted_lines(lines: Iterable[str]) -> Iterator[tuple[str, dict[str, int]]]:
    """Lazily yield (redacted_line, counts) for each input line."""
    # TODO: yield lazily using redact_line
    _ = redact_line
    if False:
        yield "", {}


def redact_log_file(src: Path, dest: Path, stats_dest: Path) -> dict[str, int]:
    """Stream-redact `src` -> `dest`, atomically write JSON stats to `stats_dest`, return stats."""
    # TODO: stream line-by-line, accumulate totals, write atomic JSON stats
    return {"lines": 0, "emails": 0, "cpfs": 0, "bearers": 0}
