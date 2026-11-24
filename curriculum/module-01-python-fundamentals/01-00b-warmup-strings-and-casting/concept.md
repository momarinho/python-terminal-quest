## Beginner Warm-Up 2: Strings & Type Conversion

In real Python scripts, user input and environment variables arrive as plain text (`str`). Here are the 3 everyday tools to clean and convert them safely:

### 1. `.strip().lower()`
```python
def clean_label(raw: str) -> str:
    return raw.strip().lower()
```

### 2. Casting Text to Numbers (`int(...)`)
```python
def parse_count(raw: str) -> int:
    return int(raw.strip())
```

### 3. Safe Boolean Text Check (`in {"true", "1", "yes"}`)
Remember: `bool("false")` is `True`! Check membership instead:
```python
def is_enabled(raw: str) -> bool:
    return raw.strip().lower() in {"true", "1", "yes"}
```

### Challenge
Complete `clean_label`, `parse_count`, and `is_enabled` in `warmup.py`.
