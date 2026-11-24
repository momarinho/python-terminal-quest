## Concept: Warm-Up & Quick Syntax Reveal (Module 1)

Before tackling full parsing challenges, warm up your fingers with **three 1-line Python patterns** you will use everywhere in this module. Feel free to peek at the exact pattern revealed below!

### Pattern Reveal #1 — Cleaning Whitespace & Casing
```python
def clean_label(raw: str) -> str:
    return raw.strip().lower()
```

### Pattern Reveal #2 — Casting Strings to `int`
```python
def parse_count(raw: str) -> int:
    return int(raw.strip())
```

### Pattern Reveal #3 — Explicit `bool` Normalization (Not `bool("false")`)
```python
def is_enabled(raw: str) -> bool:
    return raw.strip().lower() in {"true", "1", "yes"}
```

### Challenge
Open `warmup.py` and complete `clean_label`, `parse_count`, and `is_enabled` (each is 1 line!).
