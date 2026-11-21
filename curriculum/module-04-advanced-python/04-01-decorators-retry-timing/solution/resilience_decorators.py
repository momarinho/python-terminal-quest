import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry_on(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int = 3,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry the decorated callable up to `max_attempts` times on `exceptions`."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts:
                        raise
            raise AssertionError("Unreachable")

        return wrapper

    return decorator


def record_timing(
    sink: list[tuple[str, float]],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Record (function_name, elapsed_seconds) into `sink` using time.perf_counter()."""

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                sink.append((fn.__name__, time.perf_counter() - start))

        return wrapper

    return decorator
