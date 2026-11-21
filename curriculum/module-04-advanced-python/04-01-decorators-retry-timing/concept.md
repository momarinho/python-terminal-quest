## Concept: Decorators & `@functools.wraps`

A decorator wraps a function to add cross-cutting behavior (logging, timing, retries, authorization) without modifying its core business logic.

### Preserving Function Metadata with `@functools.wraps`
Without `@functools.wraps(fn)`, a wrapper overwrites `fn.__name__` and `fn.__doc__` with `"wrapper"`. Parameterized decorators add one outer factory layer:

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def audit_tag(tag: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

### Challenge
Implement `retry_on(exceptions, max_attempts=3)` and `record_timing(sink)` in `resilience_decorators.py` preserving `__name__` and `__doc__`, recording elapsed time even if an exception is raised (`try`/`finally`).
