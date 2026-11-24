## Beginner Warm-Up 3: Comprehensions, `Counter` & `deque`

Three tools from Python's standard library that replace verbose manual boilerplate:

```python
from collections import Counter, deque

def double_positives(nums: list[int]) -> list[int]:
    return [n * 2 for n in nums if n > 0]

def most_common_word(words: list[str]) -> str:
    return Counter(words).most_common(1)[0][0]

def keep_recent(events: list[str], limit: int) -> list[str]:
    return list(deque(events, maxlen=limit))
```

### Challenge
Implement `double_positives`, `most_common_word`, and `keep_recent` in `warmup.py`.
