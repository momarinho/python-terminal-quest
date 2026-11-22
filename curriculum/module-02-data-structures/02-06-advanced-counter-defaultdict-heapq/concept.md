## Concept: `Counter`, `defaultdict`, and `heapq` Priority Queues

The Python standard library ships battle-tested tools in `collections` and `heapq` that eliminate boilerplate and keep algorithms `O(N log K)` or `O(N)`.

### `Counter` & `defaultdict`
* `Counter(items).most_common(k)` tallies hashable items in one pass.
* `defaultdict(list)` automatically creates an empty list on first key access—no `if key not in groups:` needed!

### `heapq` Min-Heap & Deterministic Tie-Breaking
`heapq` maintains a **min-heap** on a standard `list` (`heappush`, `heappop` in `O(log N)`).
* To break ties cleanly by insertion order (FIFO for equal priority), store `(priority, seq, payload)` tuples—where `seq` is a monotonically increasing integer so `payload` itself never gets compared!

```python
import heapq

hold_queue: list[tuple[int, int, str]] = []
heapq.heappush(hold_queue, (1, 0, "book-A"))
heapq.heappush(hold_queue, (1, 1, "book-B"))
_, _, first = heapq.heappop(hold_queue)  # "book-A"
```

### Challenge
Implement `top_error_codes`, `group_alerts_by_service`, and `IncidentPriorityQueue` in `incident_triage.py`.
