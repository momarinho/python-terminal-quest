import pytest
from telemetry_windows import (
    every_nth_sample,
    moving_window_averages,
    normalize_latencies,
    recent_tail,
)


def test_recent_tail_handles_zero_and_oversized_counts() -> None:
    data = [10, 20, 30, 40]
    assert recent_tail(data, 2) == [30, 40]
    assert recent_tail(data, 10) == [10, 20, 30, 40]
    assert recent_tail(data, 0) == []
    assert recent_tail(data, -3) == []
    assert data == [10, 20, 30, 40]


def test_every_nth_sample_and_validation() -> None:
    assert every_nth_sample([1, 2, 3, 4, 5], 2) == [1, 3, 5]
    with pytest.raises(ValueError):
        every_nth_sample([1, 2], 0)


def test_normalize_latencies_filters_and_clamps() -> None:
    raw = [-5, 12, 250, 0, -1, 180]
    assert normalize_latencies(raw, 200) == [12, 200, 0, 180]
    assert raw == [-5, 12, 250, 0, -1, 180]


def test_moving_window_averages_and_bounds() -> None:
    src = [10, 20, 30, 45]
    assert moving_window_averages(src, 2) == [15.0, 25.0, 37.5]
    assert moving_window_averages([1, 2, 3], 3) == [2.0]
    assert moving_window_averages([1, 2], 3) == []
    assert src == [10, 20, 30, 45]
    with pytest.raises(ValueError):
        moving_window_averages(src, 0)
