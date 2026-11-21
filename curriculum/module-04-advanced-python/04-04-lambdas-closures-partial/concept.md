## Concept: Closures, Late-Binding Traps & `functools.partial`

Closures remember variables from their enclosing scope—which can surprise you inside `for` loops!

### The Late-Binding Loop Closure Trap
```python
# BUG: every lambda captures the SAME loop variable `i` by reference!
handlers = [lambda: i for i in range(3)]
# [h() for h in handlers] -> [2, 2, 2]

# FIX: bind the value eagerly with functools.partial or a default arg:
from functools import partial
def emit(val: int) -> int:
    return val
handlers = [partial(emit, i) for i in range(3)]
```

### `nonlocal` State & `functools.partial`
* Use `nonlocal count` inside an inner function when rebinding a scalar variable from the enclosing function.
* `functools.partial(fn, *args, **kwargs)` creates clean, inspectable callbacks with pre-filled arguments—prefer it over complex lambdas.

### Challenge
Fix the late-binding loop trap in `build_threshold_checks`, implement `make_moving_counter` (using `nonlocal`), and build `bind_alert_formatter` (using `functools.partial`) in `callbacks.py`.
