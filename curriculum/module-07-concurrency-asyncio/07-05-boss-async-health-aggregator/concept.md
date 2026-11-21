## Boss Fight: Resilient Async Health Aggregator

API gateways aggregate health probes across dozens of downstream services concurrently without letting one stalled service block the gateway or overload upstream pods.

### Multi-File Architecture (`client.py` + `aggregator.py`)
1. **`client.py` -> `ProbeClient`**
   * Initialized with `client: httpx.AsyncClient`, `max_concurrency: int = 4`, `per_probe_timeout: float = 0.5`, `max_retries: int = 1`, `sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep`.
   * `probe(service: str, url: str) -> dict[str, object]`:
     * Guard concurrency with `asyncio.Semaphore(max_concurrency)` and wrap each attempt with `asyncio.timeout(per_probe_timeout)`.
     * Retry up to `max_retries` times on `503` or `TimeoutError` / `httpx.TimeoutException`.
     * Return `{"service": service, "status": "UP", "latency_ms": int(...), "error": None}` on HTTP `200` with JSON `{"ok": True}` (or `"DEGRADED"` if HTTP `200` with `{"ok": False}`).
     * Return `{"service": service, "status": "DOWN", "latency_ms": None, "error": <reason>}` if retries exhaust or a non-200 error occurs (never crash sibling probes!).
2. **`aggregator.py` -> `HealthAggregator(probe_client: ProbeClient)`**
   * `check_cluster(targets: dict[str, str]) -> dict[str, object]`:
     * Fan out across `targets` (`{service_name: url}`) using `asyncio.TaskGroup`.
     * Compute overall `"overall"`: `"UP"` if all targets are `"UP"`, `"DEGRADED"` if at least one is `"UP"` or `"DEGRADED"` and at least one is not `"UP"`, else `"DOWN"` (if empty targets, `"UP"`).
     * Return `{"overall": ..., "up_count": ..., "down_count": ..., "services": sorted_list_by_service_name}`.
