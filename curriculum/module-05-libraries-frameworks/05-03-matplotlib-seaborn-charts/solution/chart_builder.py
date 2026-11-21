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
    if not services or len(services) != len(p95_ms):
        raise ValueError("services and p95_ms must be non-empty and equal length")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    try:
        sns.barplot(x=services, y=p95_ms, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Service")
        ax.set_ylabel("p95 (ms)")
        for idx, val in enumerate(p95_ms):
            ax.text(idx, val, f"{val:.1f}", ha="center", va="bottom", fontsize=9)
        fig.tight_layout()
        fig.savefig(output_path, dpi=120)
        return output_path
    finally:
        plt.close(fig)
