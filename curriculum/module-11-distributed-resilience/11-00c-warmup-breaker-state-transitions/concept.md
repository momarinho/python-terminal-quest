## Beginner Warm-Up 3: Circuit Breaker State Basics

A circuit breaker stops hammering a failing dependency once consecutive failures reach a threshold:

```python
class SimpleBreaker:
    def __init__(self, threshold: int = 3) -> None:
        self.threshold = threshold
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.state = "OPEN"

    def record_success(self) -> None:
        self.failures = 0
        self.state = "CLOSED"
```

### Challenge
Complete `record_failure()` and `record_success()` in `warmup.py`.
