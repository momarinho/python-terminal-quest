## Concept: Warm-Up & Quick Syntax Reveal (Module 5)

Module 5 tours Python's data and web ecosystem (NumPy, Pandas, Matplotlib, Flask, Requests, BS4, Django). Warm up with vectorized NumPy and Pandas first!

### Pattern Reveal #1 — Vectorized Multiplication
```python
import numpy as np

def scale_array(values: list[float], factor: float) -> list[float]:
    return (np.asarray(values, dtype=float) * factor).tolist()
```

### Pattern Reveal #2 — Boolean Mask Filtering
```python
def filter_above_threshold(values: list[int], threshold: int) -> list[int]:
    arr = np.asarray(values)
    return arr[arr > threshold].tolist()
```

### Pattern Reveal #3 — Summing a DataFrame Column Safely
```python
import pandas as pd

def total_column_sum(rows: list[dict[str, int]], col: str) -> int:
    df = pd.DataFrame(rows)
    return int(df[col].sum()) if not df.empty else 0
```

### Challenge
Open `warmup.py` and complete `scale_array`, `filter_above_threshold`, and `total_column_sum`.
