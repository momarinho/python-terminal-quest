import tracemalloc

import pytest
from profiler_tools import profile_memory_peak, profile_top_functions


def test_profile_memory_peak_captures_allocation_and_restores_state() -> None:
    assert tracemalloc.is_tracing() is False

    def allocate_payload() -> int:
        buf = [bytearray(1024) for _ in range(100)]
        return len(buf)

    metrics = profile_memory_peak(allocate_payload)
    assert metrics["result"] == 100
    assert int(metrics["peak_bytes"]) >= 100 * 1024  # type: ignore[arg-type]
    assert tracemalloc.is_tracing() is False


def test_profile_top_functions_returns_sorted_cprofile_hotspots() -> None:
    def inner_work() -> int:
        return sum(i * i for i in range(5000))

    def outer_work() -> int:
        return inner_work() + inner_work()

    top = profile_top_functions(outer_work, limit=3)
    assert len(top) >= 2
    assert len(top) <= 3
    names = [item[0] for item in top]
    assert "outer_work" in names
    assert all(top[i][2] >= top[i + 1][2] for i in range(len(top) - 1))

    with pytest.raises(ValueError):
        profile_top_functions(outer_work, limit=0)
