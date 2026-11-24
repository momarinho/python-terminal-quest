## Concept: Warm-Up & Quick Syntax Reveal (Module 2)

Module 2 explores sequences, hash maps, queues, and heaps. Let's reveal the **3 foundational 1-line idioms** first so they feel effortless!

### Pattern Reveal #1 — Negative Slicing (`items[-2:]`)
```python
def last_two(items: list[int]) -> list[int]:
    return items[-2:]
```

### Pattern Reveal #2 — Filtered List Comprehension
```python
def square_positives(nums: list[int]) -> list[int]:
    return [n * n for n in nums if n > 0]
```

### Pattern Reveal #3 — Safe Dictionary Lookup (`.get(key, 0)`)
```python
def safe_lookup(mapping: dict[str, int], key: str) -> int:
    return mapping.get(key, 0)
```

### Challenge
Open `warmup.py` and replace the 3 placeholder return values using the syntax patterns above.
