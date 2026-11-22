## Concept: Generators & Lazy `O(1)` Memory Pipelines

Materializing intermediate `[...]` lists at every stage of an ETL pipeline forces the entire dataset into RAM. Generators (`yield`) and `itertools` compute **one item on demand**.

### Streaming `yield` & `itertools.batched` / `islice`
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
* Python 3.12+ includes `itertools.batched(iterable, n)` to yield fixed-size tuple chunks lazily without loading the stream into a list!
* Use `itertools.islice(iter, n)` instead of slicing (`list(iter)[:n]`) so upstream generators stop pulling once `n` items are consumed.
* Note: a generator is **single-pass**; callers consume it incrementally via `next()`, `islice()`, or `for`.

### Challenge
Implement `iter_non_empty_events`, `iter_error_records`, and `batch_records` as true lazy generators/iterators in `lazy_pipeline.py`.
