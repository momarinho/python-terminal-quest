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
    # TODO: fetch -> parse -> pandas groupby -> Agg PNG chart (close fig) -> Markdown report
    _ = (plt, sns, fetch_html, parse_metrics_table, chart_path, report_path)
    return pd.DataFrame(columns=["region", "avg_latency_ms", "service_count"])
