## Concept: Python Data Model & Magic (Dunder) Methods

Python's operators (`==`, `<`), built-ins (`len()`, `sorted()`, `repr()`), and `for` loops delegate directly to double-underscore ("dunder") methods.

### Value Equality, Hashing & Ordering
* `__repr__` should return an unambiguous developer string, e.g., `f"Ticket({self.priority}, {self.code!r})"`.
* If you define `__eq__`, Python sets `__hash__ = None` unless you also define `__hash__` (two equal objects **must** produce identical hashes so they work in `set` and `dict`!).
* Always return `NotImplemented` from `__eq__` and `__lt__` when `other` is not a compatible type.

```python
from collections.abc import Iterator
from functools import total_ordering

@total_ordering
class PriorityTicket:
    def __init__(self, priority: int, code: str) -> None:
        self.priority = priority
        self.code = code

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PriorityTicket):
            return NotImplemented
        return (self.priority, self.code) == (other.priority, other.code)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PriorityTicket):
            return NotImplemented
        return (self.priority, self.code) < (other.priority, other.code)

    def __hash__(self) -> int:
        return hash((self.priority, self.code))
```

### Container Protocol (`__len__`, `__iter__`)
Implementing `__len__` and `__iter__(self) -> Iterator[T]` lets callers pass your object to `len(container)`, `for item in container:`, and `list(container)`.

### Challenge
Implement `SemVer` (`__repr__`, `__str__`, `__eq__`, `__hash__`, `__lt__`) and `ReleaseQueue` (`add`, `__len__`, `__iter__` yielding sorted versions) in `semver.py`.
