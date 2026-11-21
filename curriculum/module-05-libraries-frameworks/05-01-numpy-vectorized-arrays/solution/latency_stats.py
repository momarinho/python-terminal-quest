import numpy as np
from numpy.typing import NDArray


def summarize_latencies(samples: list[float]) -> dict[str, float | int]:
    """Filter non-negative latencies and return count, mean, p95, and p99."""
    arr = np.asarray(samples, dtype=np.float64)
    valid = arr[arr >= 0.0]
    if valid.size == 0:
        raise ValueError("No valid non-negative latency samples")
    return {
        "count": int(valid.size),
        "mean": round(float(np.mean(valid)), 4),
        "p95": round(float(np.percentile(valid, 95)), 4),
        "p99": round(float(np.percentile(valid, 99)), 4),
    }


def minmax_scale(values: list[float]) -> NDArray[np.float64]:
    """Scale numeric values to [0.0, 1.0]; return zeros if constant array, ValueError if empty."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("values must not be empty")
    lo = float(arr.min())
    hi = float(arr.max())
    if hi == lo:
        return np.zeros_like(arr, dtype=np.float64)
    return (arr - lo) / (hi - lo)
