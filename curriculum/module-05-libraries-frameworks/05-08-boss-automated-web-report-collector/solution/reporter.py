from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fetcher import fetch_html
from parser import parse_metrics_table


def build_report(url: str, chart_path: Path, report_path: Path) -> pd.DataFrame:
    """Fetch HTML metrics, aggregate by region in pandas, render Agg PNG chart and Markdown report."""
    html = fetch_html(url)
    rows = parse_metrics_table(html)
    if not rows:
        raise ValueError("No valid metric rows found in HTML")

    df = pd.DataFrame(rows)
    summary = (
        df.groupby("region", as_index=False)
        .agg(
            avg_latency_ms=("latency_ms", "mean"),
            service_count=("service", "count"),
        )
        .sort_values(by=["avg_latency_ms", "region"], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary["avg_latency_ms"] = summary["avg_latency_ms"].round(2)
    summary["service_count"] = summary["service_count"].astype(int)

    chart_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    try:
        sns.barplot(data=summary, x="region", y="avg_latency_ms", ax=ax)
        ax.set_title("Average Latency by Region")
        ax.set_xlabel("Region")
        ax.set_ylabel("Avg Latency (ms)")
        fig.tight_layout()
        fig.savefig(chart_path, dpi=120)
    finally:
        plt.close(fig)

    lines = [
        "# Regional Latency Digest",
        "",
        "| Region | Avg Latency (ms) | Services |",
        "| :--- | ---: | ---: |",
    ]
    for row in summary.itertuples(index=False):
        lines.append(f"| {row.region} | {row.avg_latency_ms:.2f} | {row.service_count} |")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary
