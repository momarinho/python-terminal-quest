## Beginner Warm-Up 2: Lazy `yield` Generators

Instead of creating and returning a big `list`, `yield` produces items one at a time on demand:

```python
from collections.abc import Iterator

def iter_evens(limit: int) -> Iterator[int]:
    yield from range(0, limit + 1, 2)

def iter_non_empty(lines: list[str]) -> Iterator[str]:
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned
```

### Challenge
Implement `iter_evens` and `iter_non_empty` in `warmup.py`.
