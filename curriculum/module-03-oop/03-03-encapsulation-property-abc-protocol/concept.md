## Concept: `@property` Encapsulation & `ABC` vs. `typing.Protocol`

Python hides internal state via convention (`_attr`) and `@property` descriptors—allowing validated writes or read-only views without breaking clean attribute syntax.

### `@property` Validation
```python
class Thermostat:
    def __init__(self, target_c: float) -> None:
        self._target_c = 20.0
        self.target_c = target_c  # routes through setter!

    @property
    def target_c(self) -> float:
        return self._target_c

    @target_c.setter
    def target_c(self, value: float) -> None:
        if not (10.0 <= value <= 35.0):
            raise ValueError("Target out of safe range")
        self._target_c = value
```

### `ABC` (Nominal) vs. `typing.Protocol` (Structural Duck Typing)
* Inherit from `abc.ABC` with `@abstractmethod` when subclasses share base machinery and must explicitly opt in.
* Use `typing.Protocol` (`@runtime_checkable` if needed) for pure **structural interfaces**: any class implementing the required method signature satisfies the contract *without* inheriting from a base class!

### Challenge
Implement `TokenBucket` (encapsulated `_tokens` and validated `refill_rate` `@property`), `MetricsSink(Protocol)`, `MemoryMetricsSink`, and `record_bucket_metrics` in `rate_limiter.py`.
