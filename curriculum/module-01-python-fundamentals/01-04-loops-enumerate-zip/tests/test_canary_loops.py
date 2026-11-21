import pytest
from canary_loops import (
    first_degraded_stage,
    pair_node_latencies,
    simulate_backoff_attempts,
)


def test_pair_node_latencies_strict_zip() -> None:
    assert pair_node_latencies(["n1", "n2"], [12, 45]) == ["n1:12ms", "n2:45ms"]
    with pytest.raises(ValueError):
        pair_node_latencies(["n1", "n2"], [12])


def test_first_degraded_stage_uses_one_based_index() -> None:
    assert first_degraded_stage([0.01, 0.02, 0.08, 0.12], 0.05) == 3
    assert first_degraded_stage([0.01, 0.05], 0.05) is None


def test_simulate_backoff_attempts_respects_budget_and_cap() -> None:
    # 100 + 200 + 400 = 700 <= 800; next 800 exceeds remaining 100
    assert simulate_backoff_attempts(100, 5, 800) == [100, 200, 400]
    assert simulate_backoff_attempts(100, 2, 1000) == [100, 200]
    assert simulate_backoff_attempts(100, 3, 50) == []
