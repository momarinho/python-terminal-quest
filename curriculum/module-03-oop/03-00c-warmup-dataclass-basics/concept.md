## Beginner Warm-Up 3: `@dataclass(frozen=True)`

`@dataclass` generates `__init__`, `__repr__`, and `==` for free. Adding `frozen=True` makes instances safely immutable:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Badge:
    name: str
    points: int = 10
```

### Challenge
Open `warmup.py`, fix `Badge.points` default to `10`, and complete `format_badge` + `add_tag`.
