import pytest
from consumer import EventConsumer, compute_backoff_seconds


def test_backoff_is_exponential_and_capped() -> None:
    assert compute_backoff_seconds(0, base_seconds=0.5, cap_seconds=4.0) == 0.5
    assert compute_backoff_seconds(1, base_seconds=0.5, cap_seconds=4.0) == 1.0
    assert compute_backoff_seconds(3, base_seconds=0.5, cap_seconds=4.0) == 4.0
    assert compute_backoff_seconds(8, base_seconds=0.5, cap_seconds=4.0) == 4.0
    with pytest.raises(ValueError):
        compute_backoff_seconds(-1)


def test_deduplication_and_dlq_quarantine() -> None:
    handled: list[str] = []

    def handler(event_id: str, payload: dict[str, object]) -> None:
        if payload.get("poison"):
            raise ValueError("invalid schema")
        handled.append(event_id)

    consumer = EventConsumer(handler, max_attempts=3)

    assert consumer.consume("evt-1", {"ok": True}) == "PROCESSED"
    assert consumer.consume("evt-1", {"ok": True}) == "DUPLICATE"
    assert handled == ["evt-1"]

    assert consumer.consume("evt-bad", {"poison": True}) == "RETRY"
    assert consumer.consume("evt-bad", {"poison": True}) == "RETRY"
    assert consumer.consume("evt-bad", {"poison": True}) == "DLQ"

    assert len(consumer.dlq) == 1
    assert consumer.dlq[0].event_id == "evt-bad"
    assert consumer.dlq[0].attempts == 3
    assert "invalid schema" in consumer.dlq[0].reason
