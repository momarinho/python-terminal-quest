## Beginner Warm-Up 3: JSON & URL Query Strings

Web APIs speak JSON payloads and URL query parameters:

```python
import json
from urllib.parse import urlencode

def decode_status(raw_json: str) -> str:
    data = json.loads(raw_json)
    return str(data.get("status", "unknown"))

def build_query_url(base_url: str, params: dict[str, str]) -> str:
    return f"{base_url}?{urlencode(params)}"
```

### Challenge
Complete `decode_status` and `build_query_url` in `warmup.py`.
