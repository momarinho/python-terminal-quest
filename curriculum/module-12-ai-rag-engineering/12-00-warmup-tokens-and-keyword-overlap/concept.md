## Concept: Warm-Up & Quick Syntax Reveal (Module 12)

Before building full hybrid retrieval and guardrails, practice the **3 tiny primitives** used inside every AI pipeline!

### Pattern Reveal #1 — Fast Token Estimator (`~4 chars/token`)
```python
import math

def estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / 4) if text else 0
```

### Pattern Reveal #2 — API Key Scrubbing (`re.sub`)
```python
import re

def redact_api_key(text: str) -> str:
    return re.sub(r"sk-[A-Za-z0-9]{6,}", "[REDACTED]", text)
```

### Pattern Reveal #3 — Simple Lexical Retrieval Overlap
```python
def keyword_overlap_score(query: str, doc: str) -> float:
    q_words = set(re.findall(r"[a-z0-9]+", query.lower()))
    d_words = set(re.findall(r"[a-z0-9]+", doc.lower()))
    return (len(q_words & d_words) / len(q_words)) if q_words else 0.0
```

### Challenge
Open `warmup.py` and complete `estimate_tokens`, `redact_api_key`, and `keyword_overlap_score`.
