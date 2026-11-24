import numpy as np
import pandas as pd


def scale_array(values: list[float], factor: float) -> list[float]:
    """Multiply every value by factor using NumPy and return a Python list."""
    return (np.asarray(values, dtype=float) * factor).tolist()


def filter_above_threshold(values: list[int], threshold: int) -> list[int]:
    """Return values strictly greater than threshold using a NumPy boolean mask."""
    arr = np.asarray(values)
    return arr[arr > threshold].tolist()


def total_column_sum(rows: list[dict[str, int]], col: str) -> int:
    """Return integer sum of `col` across rows using Pandas (0 if empty)."""
    df = pd.DataFrame(rows)
    return int(df[col].sum()) if not df.empty else 0
