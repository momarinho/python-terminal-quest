## Concept: Vectorized Computing with `numpy`

NumPy stores homogeneous numbers in contiguous C memory buffers (`ndarray`), letting arithmetic, filtering, and statistical aggregations run in vectorized native code rather than Python bytecode loops.

### Boolean Masks, Percentiles & Normalization
```python
import numpy as np

temps = np.asarray([18.0, -999.0, 22.5, 25.0], dtype=np.float64)
valid = temps[temps > -100.0]                  # boolean mask filtering
p90 = float(np.percentile(valid, 90))          # percentile interpolation
spread = valid.max() - valid.min()
scaled = (valid - valid.min()) / spread if spread > 0 else np.zeros_like(valid)
```

* Always guard zero-variance arrays (`max == min`) before dividing during normalization to avoid `NaN`!
* Convert scalar outputs explicitly with `float(...)` / `int(...)` when returning standard Python types.

### Challenge
Implement `summarize_latencies` (filtering valid `>= 0` readings and computing `count`, `mean`, `p95`, `p99`) and `minmax_scale` in `latency_stats.py`.
