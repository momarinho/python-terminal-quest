## Concept: Deterministic Cleanup with Context Managers

Python's `with` statement guarantees teardown code runs whether the body finishes normally or raises an exception.

### Class-Based vs. `@contextlib.contextmanager`
* **Class-based:** Implement `__enter__(self)` and `__exit__(self, exc_type, exc, tb) -> bool | None`. Returning `True` suppresses the exception; returning `False` or `None` lets it propagate cleanly after cleanup.
* **Generator-based (`@contextmanager`):** Setup runs before `yield`, and cleanup runs inside `try: yield value ... finally: cleanup()`.

```python
from collections.abc import Iterator
from contextlib import contextmanager

@contextmanager
def temporary_valve(log: list[str], name: str) -> Iterator[str]:
    log.append(f"OPEN:{name}")
    try:
        yield name
    finally:
        log.append(f"CLOSE:{name}")
```

### Challenge
Implement `TransactionScope` (`__enter__`/`__exit__` recording `"BEGIN"`, `"COMMIT"`, or `"ROLLBACK"`) and `scoped_env_override(env, updates)` (`@contextmanager` restoring modified/added keys in `finally`) in `resource_guard.py`.
