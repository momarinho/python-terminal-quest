import pytest
from parser import parse_log_line
from tracker import SlidingWindowTopK


def test_parse_log_line_supports_any_field_order() -> None:
    assert parse_log_line("service=auth status=503 ts=100 latency_ms=42") == (
        100,
        "auth",
        503,
        42,
    )
    with pytest.raises(ValueError):
        parse_log_line("ts=100 service=auth")


def test_sliding_window_evicts_expired_and_ranks_topk() -> None:
    tracker = SlidingWindowTopK(window_seconds=60)
    tracker.ingest("ts=100 service=auth status=502 latency_ms=15")
    tracker.ingest("ts=110 service=auth status=503 latency_ms=20")
    tracker.ingest("ts=120 service=billing status=500 latency_ms=30")
    tracker.ingest("ts=130 service=search status=200 latency_ms=5")
    assert tracker.active_count() == 4
    assert tracker.top_failing_services(2) == [("auth", 2), ("billing", 1)]

    # Advance to ts=175 -> cutoff = 115, so ts=100 & ts=110 (both auth 5xx!) are evicted
    tracker.ingest("ts=175 service=checkout status=503 latency_ms=40")
    assert tracker.active_count() == 3
    assert tracker.service_summary("auth") == {"requests": 0, "errors": 0}
    assert tracker.top_failing_services(3) == [("billing", 1), ("checkout", 1)]
