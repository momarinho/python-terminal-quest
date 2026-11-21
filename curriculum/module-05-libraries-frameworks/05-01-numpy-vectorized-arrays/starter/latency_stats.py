import numpy as np
from numpy.typing import NDArray


def summarize_latencies(samples: list[float]) -> dict[str, float | int]:
    """Filter non-negative latencies and return count, mean, p95, and p99."""
    # TODO: convert to float64 ndarray, filter >= 0, raise ValueError if empty
    _ = np
    return {"count": 0, "mean": 0.0, "p95": 0.0, "p99": 0.0}


def minmax_scale(values: list[float]) -> NDArray[np.float64]:
    """Scale numeric values to [0.0, 1.0]; return zeros if constant array, ValueError if empty."""
    # TODO: vectorized (arr - lo) / (hi - lo) with zero-range guard
    return np.asarray([], dtype=np.float64)
