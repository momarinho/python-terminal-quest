## Boss Fight: Log Stream Sliding-Window Queue & Top-K Tracker

Centralized log pipelines ingest thousands of structured HTTP events per second. To trigger real-time alerts without `O(N²)` scans, you need an `O(1)` sliding time window paired with fast frequency tracking and deterministic Top-K ranking.

### Architecture (`parser.py` + `tracker.py`)
1. **`parser.py` -> `parse_log_line(line: str) -> tuple[int, str, int, int]`**
   * Parse space-separated `ts=<int> service=<str> status=<int> latency_ms=<int>` lines (fields may appear in any order).
   * Return `(ts, service, status, latency_ms)`. Raise `ValueError` on missing fields, non-integer numeric fields, or negative timestamps/latencies.
2. **`tracker.py` -> `SlidingWindowTopK`**
   * Initialized with `window_seconds: int` (`>= 1`).
   * `ingest(line: str) -> None`: parse the log line, append to a `collections.deque`, advance `max_ts = max(max_ts, ts)`, and evict all entries with `entry_ts < max_ts - window_seconds` from the left in `O(1)` per eviction—updating active service request counts and 5xx (`500 <= status < 600`) error counts!
   * `active_count() -> int`: number of events currently inside the active window.
   * `top_failing_services(k: int) -> list[tuple[str, int]]`: use `heapq` (or `heapq.nsmallest`) to return the top `k` services with `error_count > 0`, ordered by `error_count` descending, then `service` name ascending!
   * `service_summary(service: str) -> dict[str, int]`: return `{"requests": ..., "errors": ...}` for the active window (zeros if absent).
