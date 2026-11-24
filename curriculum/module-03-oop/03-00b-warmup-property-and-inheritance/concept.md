## Beginner Warm-Up 2: `@property` & Inheritance

`@property` lets a method read like a simple attribute (`rect.area`), and subclasses override parent methods cleanly:

```python
class Rectangle:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> int:
        return self.width * self.height
```

### Challenge
Complete `Rectangle.area` and `AdminBadge.label()` (returning `f"[ADMIN] {self.name}"`) in `warmup.py`.
