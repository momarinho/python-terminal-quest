## Beginner Warm-Up 3: `re.search` & `pathlib.Path`

Modern Python replaces string-concatenated file paths with `pathlib.Path`:

```python
import re
from pathlib import Path

def extract_ticket_id(text: str) -> str | None:
    match = re.search(r"TKT-\d+", text)
    return match.group(0) if match else None

def save_text_file(target: Path, content: str) -> None:
    target.write_text(content, encoding="utf-8")
```

### Challenge
Implement `extract_ticket_id` and `save_text_file` in `warmup.py`.
