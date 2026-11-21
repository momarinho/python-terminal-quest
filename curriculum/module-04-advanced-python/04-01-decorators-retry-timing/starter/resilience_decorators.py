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
    # TODO: validate max_attempts >= 1, wrap with @wraps(fn), retry up to max_attempts
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _ = (exceptions, max_attempts)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def record_timing(
    sink: list[tuple[str, float]],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Record (function_name, elapsed_seconds) into `sink` using time.perf_counter()."""
    # TODO: measure with time.perf_counter() and append inside finally
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _ = (sink, time)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
