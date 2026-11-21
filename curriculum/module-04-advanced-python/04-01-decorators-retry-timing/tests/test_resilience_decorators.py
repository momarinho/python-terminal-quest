import pytest
from resilience_decorators import record_timing, retry_on


def test_retry_on_retries_transient_errors_and_preserves_metadata() -> None:
    calls = 0

    @retry_on((ConnectionError,), max_attempts=3)
    def fetch_token() -> str:
        """Fetch auth token."""
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ConnectionError("transient")
        return "ok"

    assert fetch_token() == "ok"
    assert calls == 3
    assert fetch_token.__name__ == "fetch_token"
    assert fetch_token.__doc__ == "Fetch auth token."


def test_retry_on_does_not_swallow_unlisted_exceptions_or_exhaustion() -> None:
    @retry_on((TimeoutError,), max_attempts=2)
    def always_timeout() -> None:
        raise TimeoutError("boom")

    with pytest.raises(TimeoutError):
        always_timeout()


def test_record_timing_records_even_on_failure() -> None:
    timings: list[tuple[str, float]] = []

    @record_timing(timings)
    def compute(fail: bool) -> int:
        """Compute value."""
        if fail:
            raise RuntimeError("bad")
        return 42

    assert compute.__name__ == "compute"
    assert compute(False) == 42
    with pytest.raises(RuntimeError):
        compute(True)
    assert len(timings) == 2
    assert all(name == "compute" and elapsed >= 0.0 for name, elapsed in timings)
