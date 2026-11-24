## Beginner Warm-Up 1: Higher-Order Functions & `partial`

In Python, functions are objects you can pass around like variables—the foundation for decorators!

```python
from collections.abc import Callable
from functools import partial

def apply_twice(fn: Callable[[int], int], value: int) -> int:
    return fn(fn(value))

def multiply(a: int, b: int) -> int:
    return a * b

def make_multiplier(factor: int) -> Callable[[int], int]:
    return partial(multiply, factor)
```

### Challenge
Complete `apply_twice` and `make_multiplier` in `warmup.py`.
