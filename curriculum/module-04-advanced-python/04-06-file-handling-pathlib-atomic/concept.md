## Concept: `pathlib.Path`, Streaming CSV/JSONL & Atomic Writes

Writing directly to `target.write_text(...)` risks leaving a half-written corrupt file if the process crashes mid-write.

### Atomic Write Pattern (`tempfile` + `os.replace`)
Write to a temporary file **in the same directory** as `target` (so it lives on the same filesystem), flush, and atomically swap via `os.replace(tmp_path, target)`:

```python
import os
from pathlib import Path
import tempfile

def atomic_write_text(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=target.parent, prefix=".tmp_")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path, target)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
```

### Streaming CSV & JSON Lines
Always open CSV files with `newline=""` (`path.open("r", encoding="utf-8", newline="")`) so `csv.DictReader` handles CRLF/LF cleanly.

### Challenge
Implement `atomic_write_json`, `stream_csv_totals`, and `write_jsonl_records` in `file_ops.py`.
