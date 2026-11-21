from pathlib import Path

import matplotlib.pyplot as plt
import pytest
from chart_builder import render_latency_chart


def test_render_latency_chart_writes_valid_png_and_closes_figures(tmp_path: Path) -> None:
    before_figs = set(plt.get_fignums())
    target = tmp_path / "charts" / "latency.png"
    out = render_latency_chart(["auth", "billing", "search"], [24.5, 81.2, 15.0], target)
    assert out == target
    assert target.exists()
    data = target.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(data) > 1000
    assert set(plt.get_fignums()) == before_figs


def test_render_latency_chart_validates_inputs(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        render_latency_chart([], [], tmp_path / "empty.png")
    with pytest.raises(ValueError):
        render_latency_chart(["a", "b"], [1.0], tmp_path / "mismatch.png")
