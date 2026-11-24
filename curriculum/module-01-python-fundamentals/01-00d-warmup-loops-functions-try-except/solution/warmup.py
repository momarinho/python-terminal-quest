def sum_positives(numbers: list[int]) -> int:
    """Return the sum of numbers greater than 0."""
    total = 0
    for n in numbers:
        if n > 0:
            total += n
    return total


def parse_int_or_default(raw: str, default: int = 0) -> int:
    """Parse raw as an int, or return default if ValueError occurs."""
    try:
        return int(raw.strip())
    except ValueError:
        return default
