import cProfile
import pstats
import tracemalloc
from collections.abc import Callable


def profile_memory_peak[T](fn: Callable[[], T]) -> dict[str, object]:
    """Run `fn()` under tracemalloc and return {'result', 'current_bytes', 'peak_bytes'}."""
    # TODO: check tracemalloc.is_tracing(), start/stop cleanly, return result + memory metrics
    _ = tracemalloc
    return {"result": fn(), "current_bytes": 0, "peak_bytes": 0}


def profile_top_functions(
    fn: Callable[[], object],
    limit: int = 3,
) -> list[tuple[str, int, float]]:
    """Profile `fn()` with cProfile and return top `limit` (func_name, ncalls, cumtime) sorted desc."""
    # TODO: validate limit >= 1, run cProfile.Profile, sort pstats by cumtime desc
    _ = (cProfile, pstats, limit)
    return []
