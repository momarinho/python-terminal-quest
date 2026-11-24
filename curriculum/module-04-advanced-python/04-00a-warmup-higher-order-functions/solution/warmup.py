from collections.abc import Callable
from functools import partial


def multiply(a: int, b: int) -> int:
    return a * b


def apply_twice(fn: Callable[[int], int], value: int) -> int:
    """Apply fn twice: fn(fn(value))."""
    return fn(fn(value))


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a 1-arg function multiplying its input by `factor` using partial."""
    return partial(multiply, factor)
