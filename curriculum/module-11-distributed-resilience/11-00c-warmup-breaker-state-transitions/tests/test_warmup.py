from warmup import SimpleBreaker


def test_breaker_trips_at_threshold() -> None:
    breaker = SimpleBreaker(threshold=2)
    breaker.record_failure()
    assert breaker.state == "CLOSED"
    breaker.record_failure()
    assert breaker.state == "OPEN"


def test_breaker_resets_on_success() -> None:
    breaker = SimpleBreaker(threshold=2)
    breaker.record_failure()
    breaker.record_failure()
    breaker.record_success()
    assert breaker.state == "CLOSED" and breaker.failures == 0
