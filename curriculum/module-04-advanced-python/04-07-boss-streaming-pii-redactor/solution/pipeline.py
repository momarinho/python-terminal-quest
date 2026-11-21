import json
import os
import tempfile
from collections.abc import Iterable, Iterator
from pathlib import Path

from patterns import redact_line


def iter_redacted_lines(lines: Iterable[str]) -> Iterator[tuple[str, dict[str, int]]]:
    """Lazily yield (redacted_line, counts) for each input line."""
    for line in lines:
        yield redact_line(line)


def _atomic_write_json(target: Path, payload: dict[str, int]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=target.parent, prefix=".tmp_", suffix=".json")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
            fh.write("\n")
        os.replace(tmp_path, target)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def redact_log_file(src: Path, dest: Path, stats_dest: Path) -> dict[str, int]:
    """Stream-redact `src` -> `dest`, atomically write JSON stats to `stats_dest`, return stats."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    totals = {"lines": 0, "emails": 0, "cpfs": 0, "bearers": 0}
    with (
        src.open("r", encoding="utf-8") as in_fh,
        dest.open("w", encoding="utf-8") as out_fh,
    ):
        for clean_line, counts in iter_redacted_lines(in_fh):
            out_fh.write(clean_line)
            totals["lines"] += 1
            totals["emails"] += counts["emails"]
            totals["cpfs"] += counts["cpfs"]
            totals["bearers"] += counts["bearers"]

    _atomic_write_json(stats_dest, totals)
    return totals
