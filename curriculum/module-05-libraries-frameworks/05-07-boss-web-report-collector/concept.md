## Boss Fight: Automated Web Report Collector

Automated observability digests fetch HTML telemetry snapshots over HTTP, parse metrics reliably into tabular frames, summarize per-region totals, and publish both a Markdown summary and a visual PNG chart—all headless and deterministic.

### Multi-File Architecture (`fetcher.py` + `parser.py` + `reporter.py`)
1. **`fetcher.py` -> `fetch_html(url: str, timeout: float = 2.0) -> str`**
   * Use `requests.Session` with an explicit `timeout`, call `resp.raise_for_status()`, and wrap any `requests.RequestException` in `FetchError` (`raise FetchError(...) from exc`).
2. **`parser.py` -> `parse_metrics_table(html: str) -> list[dict[str, object]]`**
   * Parse `table#metrics tbody tr` rows containing 3 `<td>` cells (`region`, `service`, `latency_ms`), returning `[{"region": ..., "service": ..., "latency_ms": int(...)}]` (skip incomplete rows or non-numeric latencies).
3. **`reporter.py` -> `build_report(url: str, chart_path: Path, report_path: Path) -> pd.DataFrame`**
   * Fetch HTML via `fetch_html(url)` → parse via `parse_metrics_table(html)` → aggregate with `pandas` `groupby("region", as_index=False)` computing `avg_latency_ms` (mean, rounded to 2 decimals) and `service_count` (count), sorted by `avg_latency_ms` descending, `region` ascending.
   * Render a headless `Agg` Matplotlib/Seaborn barplot (`region` vs `avg_latency_ms`) to `chart_path` (closing the figure cleanly in `finally:`).
   * Write a Markdown summary table to `report_path` containing each region's `avg_latency_ms` and `service_count`, and return the summary `DataFrame`.
