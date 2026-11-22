## Concept: Stacks (LIFO) & Queues (`collections.deque`)

A Python `list` is great as a **LIFO stack** (`append()` and `pop()` at the end are `O(1)`), but terrible as a **FIFO queue** (`pop(0)` shifts every element in `O(N)`!).

### Why `collections.deque` Gives `O(1)` Queues & Ring Buffers
Under the hood, CPython's `list` is a contiguous array of object pointers—removing index `0` requires shifting `N - 1` pointers. By contrast, `collections.deque` is implemented as a **doubly-linked list of fixed-size memory blocks**, giving `O(1)` `append`, `appendleft`, `pop`, and `popleft` at both ends.

Passing `maxlen=K` turns `deque` into a bounded **ring buffer** that automatically evicts the oldest item when full—ideal for sliding time windows, rate limiters, and recent-history caches:

```python
from collections import deque

spooler: deque[str] = deque(maxlen=3)
for job in ["doc-1", "doc-2", "doc-3", "doc-4"]:
    spooler.append(job)
# Automatically evicts "doc-1" -> deque(["doc-2", "doc-3", "doc-4"])
```

### Bracket Balancing with a Stack
Push opening delimiters (`(`, `[`, `{`) onto a stack; when encountering a closing delimiter, verify the stack is non-empty and the top matches its pair!

### Challenge
Implement `is_balanced_expression` and `BoundedEventQueue` in `queue_buffers.py`.
