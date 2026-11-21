import csv
import json
import os
import tempfile
from collections import defaultdict
from collections.abc import Iterable
from decimal import Decimal
from pathlib import Path


def atomic_write_json(target: Path, payload: object) -> None:
    """Atomically write JSON payload to `target` via temp file in same directory + os.replace."""
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


def stream_csv_totals(csv_path: Path) -> dict[str, Decimal]:
    """Stream CSV rows ('category,amount') and accumulate exact Decimal totals per category."""
    totals: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            cat = str(row["category"]).strip()
            totals[cat] += Decimal(str(row["amount"]).strip())
    return dict(totals)


def write_jsonl_records(target: Path, records: Iterable[dict[str, object]]) -> int:
    """Stream `records` as JSON Lines to `target` and return number of records written."""
    target.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with target.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")
            count += 1
    return count
