from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def render_latency_chart(
    services: list[str],
    p95_ms: list[float],
    output_path: Path,
    title: str = "Service p95 Latency",
) -> Path:
    """Render a headless Seaborn barplot to `output_path` (PNG) and close the figure."""
    # TODO: validate inputs, create fig/ax, draw sns.barplot, annotate title & y-label, savefig, close fig
    _ = (plt, sns, title)
    return output_path
