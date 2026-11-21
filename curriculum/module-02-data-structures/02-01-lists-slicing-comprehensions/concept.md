## Concept: Lists, Slicing (`[start:stop:step]`) & Comprehensions

Python lists support expressive slicing that always returns a **shallow copy**—never mutating the original list.

### Slicing Patterns
* `items[-n:]` grabs the last `n` elements (careful: when `n == 0`, `items[-0:]` returns the entire list because `-0 == 0`!).
* `items[::step]` samples every `step`-th item (`step > 0`), and `items[::-1]` reverses a sequence cleanly.

```python
def sample_seismograph(waves: list[int], stride: int) -> list[int]:
    return [abs(w) for w in waves[::stride] if w != 0]
```

### List Comprehensions vs. `map`/`filter`
List comprehensions `[transform(x) for x in seq if condition(x)]` are more Pythonic and readable than nested `list(map(..., filter(...)))` calls.

### Challenge
Implement `recent_tail`, `every_nth_sample`, and `normalize_latencies` in `telemetry_windows.py` without mutating caller lists.
