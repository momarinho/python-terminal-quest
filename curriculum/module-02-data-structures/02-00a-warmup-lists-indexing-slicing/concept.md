## Beginner Warm-Up 1: List Indexing & Slicing

Python lists are zero-indexed, support negative indexes from the end (`items[-1]`), and slice cleanly with `[start:stop]`:

```python
def first_and_last(items: list[str]) -> tuple[str, str]:
    return (items[0], items[-1])

def last_three(items: list[int]) -> list[int]:
    return items[-3:]
```

### Challenge
Implement `first_and_last` and `last_three` in `warmup.py`.
