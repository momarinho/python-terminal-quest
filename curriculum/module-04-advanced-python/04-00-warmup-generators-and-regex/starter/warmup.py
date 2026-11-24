import re  # noqa: F401
from collections.abc import Callable, Iterator


def iter_even_numbers(limit: int) -> Iterator[int]:
    """Yield even integers from 0 up to limit inclusive."""
    # Reveal: yield from range(0, limit + 1, 2)
    if False:
        yield 0


def extract_order_id(text: str) -> str | None:
    """Return the first 'ORD-<digits>' token in text, or None."""
    # Reveal: match = re.search(r"ORD-\d+", text)
    return None


def apply_twice(fn: Callable[[int], int], value: int) -> int:
    """Apply fn to value twice: fn(fn(value))."""
    # Reveal: return fn(fn(value))
    return value
