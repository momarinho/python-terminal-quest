## Beginner Warm-Up 2: Simple Idempotent Execution

When a network retry sends the same `event_id` twice, an idempotent consumer processes it only once and replays the stored result:

```python
class SimpleDeduplicator:
    def __init__(self) -> None:
        self._results: dict[str, str] = {}

    def process_once(self, event_id: str, value: str) -> tuple[str, bool]:
        if event_id in self._results:
            return (self._results[event_id], True)  # True = replayed
        result = f"ok:{value}"
        self._results[event_id] = result
        return (result, False)
```

### Challenge
Implement `SimpleDeduplicator.process_once` in `warmup.py`.
