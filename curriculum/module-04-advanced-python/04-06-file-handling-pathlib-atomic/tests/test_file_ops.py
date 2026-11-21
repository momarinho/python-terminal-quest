import json
from decimal import Decimal
from pathlib import Path

from file_ops import atomic_write_json, stream_csv_totals, write_jsonl_records


def test_atomic_write_json_leaves_no_temp_leftovers(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "summary.json"
    atomic_write_json(out, {"ok": True, "count": 3})
    assert json.loads(out.read_text(encoding="utf-8")) == {"ok": True, "count": 3}
    assert [p.name for p in out.parent.iterdir()] == ["summary.json"]


def test_stream_csv_totals_and_write_jsonl(tmp_path: Path) -> None:
    csv_file = tmp_path / "ledger.csv"
    csv_file.write_text("category,amount\ninfra,12.10\nai,3.20\ninfra,0.90\n", encoding="utf-8")
    assert stream_csv_totals(csv_file) == {"infra": Decimal("13.00"), "ai": Decimal("3.20")}

    jsonl = tmp_path / "events.jsonl"
    written = write_jsonl_records(jsonl, ({"idx": i} for i in range(3)))
    assert written == 3
    assert [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines()] == [
        {"idx": 0},
        {"idx": 1},
        {"idx": 2},
    ]
