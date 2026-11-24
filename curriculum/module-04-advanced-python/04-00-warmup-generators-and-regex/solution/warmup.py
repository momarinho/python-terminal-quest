import re
from collections.abc import Callable, Iterator


def iter_even_numbers(limit: int) -> Iterator[int]:
    """Yield even integers from 0 up to limit inclusive."""
    yield from range(0, limit + 1, 2)


def extract_order_id(text: str) -> str | None:
    """Return the first 'ORD-<digits>' token in text, or None."""
    match = re.search(r"ORD-\d+", text)
    return match.group(0) if match else None


def apply_twice(fn: Callable[[int], int], value: int) -> int:
    """Apply fn to value twice: fn(fn(value))."""
    return fn(fn(value))
