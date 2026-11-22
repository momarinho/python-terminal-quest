## Concept: Clean String Parsing Without Regex Fragility

Python's built-in `str` methods solve most log and protocol parsing cleanly without brittle regular expressions.

### Essential Parsing Tools
* `text.removeprefix("Bearer ")` / `text.removesuffix(".log")` — safer than `.lstrip(...)` / `.rstrip(...)`, which strip *character sets* rather than exact prefixes/suffixes!
* `token.split("=", 1)` (`maxsplit=1`) — splits only on the **first** `=`, preserving any `=` inside base64 tokens or URLs.
* `key.casefold()` — stronger Unicode-aware case normalization than `.lower()`.
* `" ".join(parts)` — builds strings in `O(N)` instead of repeated `+=` concatenation.

```python
def parse_parcel_label(raw: str) -> tuple[str, str]:
    cleaned = raw.strip().removeprefix("PARCEL:")
    code, route = cleaned.split("|", 1)
    return code.strip().upper(), route.strip()
```

### Challenge
Implement `extract_bearer_token`, `parse_kv_log`, and `format_kv_line` in `kv_log_parser.py`.
