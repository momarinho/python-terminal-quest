## Beginner Warm-Up 4: Loops & Safe Parsing (`try / except`)

Let's wrap up Module 1's beginner warm-ups with loops and exception handling!

### 1. Filtering Inside a `for` Loop
```python
def sum_positives(numbers: list[int]) -> int:
    total = 0
    for n in numbers:
        if n > 0:
            total += n
    return total
```

### 2. Catching Bad Numbers with `try / except ValueError`
```python
def parse_int_or_default(raw: str, default: int = 0) -> int:
    try:
        return int(raw.strip())
    except ValueError:
        return default
```

### Challenge
Complete `sum_positives` and `parse_int_or_default` in `warmup.py`.
