def recent_tail(samples: list[int], count: int) -> list[int]:
    """Return the last `count` items without mutating `samples` (empty list if count <= 0)."""
    if count <= 0:
        return []
    return samples[-count:]


def every_nth_sample(samples: list[int], step: int) -> list[int]:
    """Return every `step`-th sample starting at index 0; raise ValueError if step < 1."""
    if step < 1:
        raise ValueError(f"step must be >= 1, got {step}")
    return samples[::step]


def normalize_latencies(raw_ms: list[int], cap_ms: int) -> list[int]:
    """Filter out negative readings and clamp remaining values to at most `cap_ms`."""
    return [min(val, cap_ms) for val in raw_ms if val >= 0]
