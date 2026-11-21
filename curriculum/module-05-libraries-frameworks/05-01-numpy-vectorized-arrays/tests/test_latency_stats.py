import numpy as np
import pytest
from latency_stats import minmax_scale, summarize_latencies


def test_summarize_latencies_filters_negatives_and_computes_percentiles() -> None:
    stats = summarize_latencies([-1.0, 10.0, 20.0, 30.0, 40.0, 100.0])
    assert stats["count"] == 5
    assert stats["mean"] == pytest.approx(40.0)
    assert stats["p95"] == pytest.approx(88.0)
    assert stats["p99"] == pytest.approx(97.6)

    with pytest.raises(ValueError):
        summarize_latencies([-5.0, -1.0])


def test_minmax_scale_normalizes_and_handles_constant_inputs() -> None:
    scaled = minmax_scale([10.0, 20.0, 30.0])
    assert np.allclose(scaled, [0.0, 0.5, 1.0])

    flat = minmax_scale([7.0, 7.0, 7.0])
    assert np.allclose(flat, [0.0, 0.0, 0.0])

    with pytest.raises(ValueError):
        minmax_scale([])
