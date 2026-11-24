from collections.abc import Iterator


def iter_evens(limit: int) -> Iterator[int]:
    """Yield even integers from 0 to limit inclusive."""
    yield from range(0, limit + 1, 2)


def iter_non_empty(lines: list[str]) -> Iterator[str]:
    """Yield stripped lines, skipping blank lines."""
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned
