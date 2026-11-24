## Beginner Warm-Up 1: Array Scaling & Mean Foundations

Before swapping loops for NumPy C-arrays in `05-01`, warm up on the exact math shape:

```python
from statistics import mean

def scale_values(values: list[float], factor: float) -> list[float]:
    return [v * factor for v in values]

def average_or_zero(values: list[float]) -> float:
    return mean(values) if values else 0.0
```

### Challenge
Complete `scale_values` and `average_or_zero` in `warmup.py`.
