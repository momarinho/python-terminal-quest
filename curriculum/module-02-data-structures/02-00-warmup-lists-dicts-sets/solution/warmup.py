def last_two(items: list[int]) -> list[int]:
    """Return the last two items without mutating the input list."""
    return items[-2:]


def square_positives(nums: list[int]) -> list[int]:
    """Return squares of numbers strictly greater than 0."""
    return [n * n for n in nums if n > 0]


def safe_lookup(mapping: dict[str, int], key: str) -> int:
    """Return mapping[key] or 0 if key is absent."""
    return mapping.get(key, 0)
