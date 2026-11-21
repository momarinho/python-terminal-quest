def recent_tail(samples: list[int], count: int) -> list[int]:
    """Return the last `count` items without mutating `samples` (empty list if count <= 0)."""
    # TODO: guard count <= 0 and slice [-count:]
    return []


def every_nth_sample(samples: list[int], step: int) -> list[int]:
    """Return every `step`-th sample starting at index 0; raise ValueError if step < 1."""
    # TODO: validate step and slice [::step]
    return []


def normalize_latencies(raw_ms: list[int], cap_ms: int) -> list[int]:
    """Filter out negative readings and clamp remaining values to at most `cap_ms`."""
    # TODO: list comprehension filtering >= 0 and clamping with min(..., cap_ms)
    return []
