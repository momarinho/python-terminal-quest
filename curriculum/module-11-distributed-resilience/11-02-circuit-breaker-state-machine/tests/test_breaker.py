import pytest
from breaker import CircuitBreaker, CircuitOpenError


def test_trips_open_after_threshold_and_fast_fails() -> None:
    now = 100.0
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=10.0, clock=lambda: now)

    def fail() -> None:
        raise OSError("upstream 503")

    # Non-consecutive failure resets on success
    with pytest.raises(OSError):
        cb.call(fail)
    assert cb.state == "CLOSED"
    assert cb.call(lambda: "ok") == "ok"
    assert cb.state == "CLOSED"

    # Two consecutive failures trip OPEN
    with pytest.raises(OSError):
        cb.call(fail)
    with pytest.raises(OSError):
        cb.call(fail)
    assert cb.state == "OPEN"

    # Upstream callable is NOT invoked while OPEN
    called = False

    def should_not_run() -> str:
        nonlocal called
        called = True
        return "nope"

    with pytest.raises(CircuitOpenError):
        cb.call(should_not_run)
    assert called is False


def test_half_open_probe_recovers_to_closed_or_retrips_open() -> None:
    now = 50.0
    cb = CircuitBreaker(failure_threshold=1, recovery_timeout=15.0, clock=lambda: now)

    def fail() -> None:
        raise RuntimeError("timeout")

    with pytest.raises(RuntimeError):
        cb.call(fail)
    assert cb.state == "OPEN"

    # Advance virtual clock past recovery_timeout -> HALF_OPEN
    now += 15.0
    assert cb.state == "HALF_OPEN"

    # Probe failure trips immediately back to OPEN
    with pytest.raises(RuntimeError):
        cb.call(fail)
    assert cb.state == "OPEN"

    # Advance again -> HALF_OPEN -> probe success closes circuit
    now += 15.0
    assert cb.state == "HALF_OPEN"
    assert cb.call(lambda: "recovered") == "recovered"
    assert cb.state == "CLOSED"
