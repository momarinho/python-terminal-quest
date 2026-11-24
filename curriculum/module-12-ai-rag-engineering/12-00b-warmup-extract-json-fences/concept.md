## Beginner Warm-Up 2: Cleaning LLM JSON Replies

LLMs love wrapping JSON inside ```` ```json ... ``` ```` markdown fences! Unwrap the `{...}` span cleanly before calling `json.loads`:

```python
import json

def parse_llm_json(raw: str) -> dict[str, object]:
    start = raw.find("{")
    end = raw.rfind("}")
    return dict(json.loads(raw[start : end + 1]))
```

### Challenge
Implement `parse_llm_json` in `warmup.py` (raising `ValueError` if no `{` / `}` object span exists).
