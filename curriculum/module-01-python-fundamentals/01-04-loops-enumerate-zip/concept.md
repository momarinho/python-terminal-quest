## Concept: Idiomatic Python Loops (`enumerate`, `zip`, `while`)

Python `for` loops iterate directly over items rather than manual index counters (`for i in range(len(items))`).

### `enumerate` & `zip(..., strict=True)`
* Use `enumerate(items, start=1)` when you need both a human-friendly 1-based index and the element.
* Use `zip(seq_a, seq_b, strict=True)` when two sequences must have identical lengths; `strict=True` raises `ValueError` instead of silently truncating mismatched inputs!

```python
def label_book_batches(titles: list[str], page_counts: list[int]) -> list[str]:
    result: list[str] = []
    for batch_num, (title, pages) in enumerate(zip(titles, page_counts, strict=True), start=1):
        result.append(f"Batch #{batch_num}: {title} ({pages}p)")
    return result
```

### Bounded `while` Loops
Whenever a `while` loop retries work or drains a queue, enforce a maximum iteration bound (or empty-collection condition) so bad state cannot hang the process.

### Challenge
Implement `pair_node_latencies`, `first_degraded_stage`, and `simulate_backoff_attempts` in `canary_loops.py`.
