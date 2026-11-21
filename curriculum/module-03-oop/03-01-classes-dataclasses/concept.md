## Concept: Classes & `@dataclass` Domain Modeling

Python's `@dataclass` decorator auto-generates `__init__`, `__repr__`, and `__eq__` from type-annotated class fields—eliminating repetitive constructor boilerplate while keeping invariants explicit.

### Frozen Records, `__post_init__`, and `default_factory`
* `@dataclass(frozen=True)` makes instances immutable (and hashable when all fields are hashable), ideal for value objects.
* `__post_init__(self)` runs right after `__init__` to validate invariants or normalize fields.
* Never write `items: list[str] = []` on a dataclass (Python rejects mutable defaults with `ValueError`)! Use `field(default_factory=list)` instead.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class LibraryBook:
    isbn: str
    title: str
    pages: int

    def __post_init__(self) -> None:
        if not self.isbn.strip() or self.pages <= 0:
            raise ValueError("Book requires non-empty ISBN and positive pages")

@dataclass
class ReadingShelf:
    name: str
    books: list[LibraryBook] = field(default_factory=list)
```

### Challenge
Implement `ServiceEndpoint` (`frozen=True`, validated in `__post_init__`) and `ClusterSnapshot` (with `field(default_factory=list)`, `register()`, and `healthy_ratio()`) in `cluster_models.py`.
