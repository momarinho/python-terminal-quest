from typing import Protocol, runtime_checkable


@runtime_checkable
class MetricsSink(Protocol):
    def emit(self, metric: str, value: int) -> None: ...


class MemoryMetricsSink:
    """Satisfies MetricsSink structurally without inheriting from it."""

    def __init__(self) -> None:
        self.events: list[tuple[str, int]] = []

    def emit(self, metric: str, value: int) -> None:
        self.events.append((metric, value))


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._tokens = capacity
        self._refill_rate = 1
        self.refill_rate = refill_rate

    @property
    def available_tokens(self) -> int:
        return self._tokens

    @property
    def refill_rate(self) -> int:
        return self._refill_rate

    @refill_rate.setter
    def refill_rate(self, value: int) -> None:
        if value <= 0:
            raise ValueError(f"refill_rate must be positive, got {value}")
        self._refill_rate = value

    def consume(self, count: int = 1) -> bool:
        if count <= 0:
            raise ValueError("count must be positive")
        if count > self._tokens:
            return False
        self._tokens -= count
        return True

    def refill(self, elapsed_seconds: int) -> int:
        if elapsed_seconds < 0:
            raise ValueError("elapsed_seconds must be non-negative")
        headroom = self._capacity - self._tokens
        added = min(headroom, elapsed_seconds * self._refill_rate)
        self._tokens += added
        return self._tokens


def record_bucket_metrics(bucket: TokenBucket, sink: MetricsSink, consumed: bool) -> None:
    sink.emit("rate_limit.allowed", 1 if consumed else 0)
    sink.emit("rate_limit.remaining", bucket.available_tokens)
