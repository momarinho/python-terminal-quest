## Beginner Warm-Up 1: Token Estimation & Secret Scrubbing

Two habits every AI engineer needs before sending prompts to any LLM:

```python
import math
import re

def estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / 4) if text else 0

def redact_api_key(text: str) -> str:
    return re.sub(r"sk-[A-Za-z0-9]{6,}", "[REDACTED]", text)
```

### Challenge
Complete `estimate_tokens` and `redact_api_key` in `warmup.py`.
