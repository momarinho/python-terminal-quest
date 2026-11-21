import json
from collections.abc import Iterable
from decimal import Decimal
from pathlib import Path


def atomic_write_json(target: Path, payload: object) -> None:
    """Atomically write JSON payload to `target` via temp file in same directory + os.replace."""
    # TODO: create parent dir, write temp file in target.parent, os.replace(tmp, target)
    _ = json


def stream_csv_totals(csv_path: Path) -> dict[str, Decimal]:
    """Stream CSV rows ('category,amount') and accumulate exact Decimal totals per category."""
    # TODO: open with newline='' and csv.DictReader
    return {}


def write_jsonl_records(target: Path, records: Iterable[dict[str, object]]) -> int:
    """Stream `records` as JSON Lines to `target` and return number of records written."""
    # TODO: write one JSON line per record lazily
    return 0
