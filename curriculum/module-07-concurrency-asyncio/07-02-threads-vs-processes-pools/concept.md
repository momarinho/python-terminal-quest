## Concept: `ThreadPoolExecutor` vs. `ProcessPoolExecutor`

Choosing the right executor depends on whether your bottleneck waits on external I/O or burns CPU cycles:

* **`ThreadPoolExecutor` (I/O-bound):** Threads share memory inside one Python process and release the GIL during network/disk waits. Shared mutations **and atomic read-reset swaps** must be protected by `threading.Lock()`!
* **`ProcessPoolExecutor` (CPU-bound):** Spawns separate OS processes—each with its own Python interpreter and GIL—enabling true multi-core parallelism for hashing, image encoding, or heavy pure-Python computation. Functions passed to `executor.map(...)` must be **picklable top-level module functions** (never `lambda`!).
* **Resilient Fan-Out:** Wrapping each `future.result()` in `try/except Exception:` lets one failing upstream call fall back cleanly without crashing sibling results.

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def resize_tile(tile_id: int) -> str:
    return f"tile-{tile_id}-ok"

with ProcessPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(resize_tile, [1, 2, 3]))
```

### Challenge
Fix `ThreadSafeCounter` (adding atomic `reset`), and implement `run_io_batch`, `run_io_batch_resilient`, and `hash_payloads_parallel` in `concurrency_pools.py`.
