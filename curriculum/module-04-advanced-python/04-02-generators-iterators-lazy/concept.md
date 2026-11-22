## Concept: Generators & Lazy `O(1)` Memory Pipelines

Materializing intermediate `[...]` lists at every stage of an ETL pipeline forces the entire dataset into RAM. Generators (`yield`) and `itertools` compute **one item on demand**.

### Streaming `yield`, Eager Validation & `itertools.batched` / `islice`
```python
from collections.abc import Iterable, Iterator
from itertools import batched, islice

def stream_active_stations(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("#"):
            yield cleaned

first_two = list(islice(stream_active_stations(raw_lines), 2))
chunks = batched(stream_active_stations(raw_lines), 100)  # Python 3.12+
```
* **Generator validation trap:** A function containing `yield` directly does **not** run its body until `next()` is called! Validate arguments (`size < 1`, `limit < 0`) in an eager outer function and return an inner generator expression or helper generator.
* Stop pulling immediately once a `limit` is reached so infinite upstream streams terminate cleanly.

### Challenge
Implement `iter_non_empty_events`, `iter_error_records`, `batch_records`, and `take_unique_messages` as true lazy generators/iterators in `lazy_pipeline.py`.
