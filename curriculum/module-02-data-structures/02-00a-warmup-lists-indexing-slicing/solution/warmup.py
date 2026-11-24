def first_and_last(items: list[str]) -> tuple[str, str]:
    """Return (first_item, last_item) from a non-empty list."""
    return (items[0], items[-1])


def last_three(items: list[int]) -> list[int]:
    """Return up to the last 3 items without modifying the input list."""
    return items[-3:]
