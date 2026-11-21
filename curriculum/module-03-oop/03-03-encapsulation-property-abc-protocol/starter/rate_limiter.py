from typing import Protocol, runtime_checkable


@runtime_checkable
class MetricsSink(Protocol):
    def emit(self, metric: str, value: int) -> None: ...


class MemoryMetricsSink:
    """Satisfies MetricsSink structurally without inheriting from it."""

    def __init__(self) -> None:
        self.events: list[tuple[str, int]] = []

    def emit(self, metric: str, value: int) -> None:
        # TODO: record (metric, value)
        pass


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
        # TODO: validate value > 0 and assign self._refill_rate
        pass

    def consume(self, count: int = 1) -> bool:
        # TODO: validate count > 0, return True and decrement if enough tokens else False
        return False

    def refill(self, elapsed_seconds: int) -> int:
        # TODO: validate elapsed_seconds >= 0, add elapsed_seconds * refill_rate clamped at _capacity
        return self._tokens


def record_bucket_metrics(bucket: TokenBucket, sink: MetricsSink, consumed: bool) -> None:
    # TODO: emit 'rate_limit.allowed' (1 or 0) and 'rate_limit.remaining' (bucket.available_tokens)
    pass
