## Concept: Generators & Lazy $O(1)$ Memory Pipelines

Materializing intermediate `[...]` lists at every stage of an ETL pipeline forces the entire dataset into RAM. Generators (`yield`) and `itertools` compute **one item on demand**.

### Streaming `yield` & `itertools.batched` / `islice`
```python
from collections.abc import Iterable, Iterator
from itertools import islice

def stream_active_stations(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("#"):
            yield cleaned

first_two = list(islice(stream_active_stations(raw_lines), 2))
```
* Python 3.12+ includes `itertools.batched(iterable, n)` to yield fixed-size chunks lazily!
* Note: a generator is **single-pass**; callers consume it incrementally via `next()`, `islice()`, or `for`.

### Challenge
Implement `iter_non_empty_events`, `iter_error_records`, and `batch_records` as true lazy generators/iterators in `lazy_pipeline.py`.
