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


def moving_window_averages(samples: list[int], window_size: int) -> list[float]:
    """Return contiguous window averages rounded to 2 decimals; raise ValueError if window_size < 1."""
    if window_size < 1:
        raise ValueError(f"window_size must be >= 1, got {window_size}")
    if len(samples) < window_size:
        return []
    return [
        round(sum(samples[i : i + window_size]) / window_size, 2)
        for i in range(len(samples) - window_size + 1)
    ]
