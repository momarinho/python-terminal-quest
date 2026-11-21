## Concept: CPython Internals, the GIL & Profiling (`tracemalloc` / `cProfile`)

Understanding how CPython manages memory and CPU threads prevents premature optimization and hidden bottlenecks.

### Refcounting, Cyclic GC & the GIL
* **Reference counting (`sys.getrefcount`):** Every `PyObject` frees immediately when its refcount hits `0`; Python's cyclic **Garbage Collector (`gc`)** breaks reference cycles (`a.ref = b; b.ref = a`).
* **The GIL (Global Interpreter Lock):** Serializes Python bytecode execution per process—meaning multi-threading shines for **I/O-bound** waits (releases the GIL during sockets/sleeps), while **CPU-bound** Python loops require multiprocessing (or C extensions like NumPy).

### Measuring Before Optimizing (`tracemalloc` & `cProfile`)
```python
import cProfile
import io
import pstats
import tracemalloc

def measure_fibonacci_memory() -> tuple[int, int]:
    tracemalloc.start()
    try:
        data = [i * i for i in range(10_000)]
        current, peak = tracemalloc.get_traced_memory()
        return len(data), peak
    finally:
        tracemalloc.stop()
```

### Challenge
Implement `profile_memory_peak(fn)` (returning `{"result": ..., "current_bytes": ..., "peak_bytes": ...}`, stopping `tracemalloc` only if this call started it!) and `profile_top_functions(fn, limit=3)` (returning top `(func_name, ncalls, cumtime)` sorted by `cumtime` desc via `cProfile.Profile` + `pstats.Stats`) in `profiler_tools.py`.
