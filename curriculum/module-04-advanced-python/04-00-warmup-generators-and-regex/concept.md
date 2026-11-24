## Concept: Warm-Up & Quick Syntax Reveal (Module 4)

Module 4 unlocks decorators, lazy `yield` streams, context managers, and compiled regexes. Practice these 3 bite-sized patterns first!

### Pattern Reveal #1 — Lazy Even Generator (`yield`)
```python
from collections.abc import Iterator

def iter_even_numbers(limit: int) -> Iterator[int]:
    for n in range(0, limit + 1, 2):
        yield n
```

### Pattern Reveal #2 — Extracting a Regex Match
```python
import re

def extract_order_id(text: str) -> str | None:
    match = re.search(r"ORD-\d+", text)
    return match.group(0) if match else None
```

### Pattern Reveal #3 — Passing a Function (`Callable`)
```python
from collections.abc import Callable

def apply_twice(fn: Callable[[int], int], value: int) -> int:
    return fn(fn(value))
```

### Challenge
Open `warmup.py` and implement `iter_even_numbers`, `extract_order_id`, and `apply_twice`.
