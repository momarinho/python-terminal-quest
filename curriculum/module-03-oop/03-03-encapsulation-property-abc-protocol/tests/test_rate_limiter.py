import pytest
from rate_limiter import (
    MemoryMetricsSink,
    MetricsSink,
    TokenBucket,
    record_bucket_metrics,
)


def test_token_bucket_property_encapsulation() -> None:
    bucket = TokenBucket(capacity=5, refill_rate=2)
    assert bucket.available_tokens == 5
    with pytest.raises(AttributeError):
        bucket.available_tokens = 10  # type: ignore[misc]
    with pytest.raises(ValueError):
        bucket.refill_rate = 0

    assert bucket.consume(4) is True
    assert bucket.available_tokens == 1
    assert bucket.consume(3) is False
    assert bucket.available_tokens == 1
    assert bucket.refill(10) == 5


def test_structural_protocol_metrics_sink() -> None:
    sink = MemoryMetricsSink()
    assert isinstance(sink, MetricsSink)
    bucket = TokenBucket(capacity=3, refill_rate=1)
    ok = bucket.consume(2)
    record_bucket_metrics(bucket, sink, ok)
    assert sink.events == [("rate_limit.allowed", 1), ("rate_limit.remaining", 1)]
