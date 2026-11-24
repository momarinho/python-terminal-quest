## Concept: Warm-Up & Quick Syntax Reveal (Module 3)

Before designing polymorphic classes and order books, let's warm up with modern Python's cleanest data modeling primitives!

### Pattern Reveal #1 — Frozen `@dataclass`
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Badge:
    name: str
    points: int = 10
```

### Pattern Reveal #2 — Formatting Attributes with f-strings
```python
def format_badge(badge: Badge) -> str:
    return f"{badge.name} (+{badge.points} XP)"
```

### Pattern Reveal #3 — Avoiding Mutable Default Arguments (`tags=None`)
```python
def add_tag(tags: list[str] | None = None) -> list[str]:
    result = list(tags) if tags is not None else []
    result.append("verified")
    return result
```

### Challenge
Open `warmup.py` and finish `Badge`, `format_badge`, and `add_tag`.
