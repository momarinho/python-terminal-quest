## Beginner Warm-Up 3: `if / elif / else` & Explicit `None`

Two essential Python decision rules every developer uses daily:

### 1. Chained `if / elif / else`
```python
def classify_temp(celsius: int) -> str:
    if celsius >= 30:
        return "HOT"
    if celsius >= 15:
        return "WARM"
    return "COLD"
```

### 2. Why `if retries:` Is Dangerous for `0`
In Python, `0` is falsy! Always use **`is None`** when `0` is a valid number:
```python
def normalize_retries(retries: int | None) -> int:
    return 3 if retries is None else retries
```

### Challenge
Complete `classify_temp` and `normalize_retries` in `warmup.py`.
