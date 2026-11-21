import cProfile
import pstats
import tracemalloc
from collections.abc import Callable


def profile_memory_peak[T](fn: Callable[[], T]) -> dict[str, object]:
    """Run `fn()` under tracemalloc and return {'result', 'current_bytes', 'peak_bytes'}."""
    already_tracing = tracemalloc.is_tracing()
    if not already_tracing:
        tracemalloc.start()
    else:
        tracemalloc.reset_peak()

    try:
        result = fn()
        current_bytes, peak_bytes = tracemalloc.get_traced_memory()
        return {
            "result": result,
            "current_bytes": current_bytes,
            "peak_bytes": peak_bytes,
        }
    finally:
        if not already_tracing:
            tracemalloc.stop()


def profile_top_functions(
    fn: Callable[[], object],
    limit: int = 3,
) -> list[tuple[str, int, float]]:
    """Profile `fn()` with cProfile and return top `limit` (func_name, ncalls, cumtime) sorted desc."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    profiler = cProfile.Profile()
    profiler.enable()
    try:
        fn()
    finally:
        profiler.disable()

    stats = pstats.Stats(profiler)
    rows: list[tuple[str, int, float]] = []
    for (_filename, _lineno, func_name), (_cc, nc, _tt, ct, _callers) in stats.stats.items():  # type: ignore[attr-defined]
        rows.append((str(func_name), int(nc), float(ct)))
    rows.sort(key=lambda item: (-item[2], item[0]))
    return rows[:limit]
