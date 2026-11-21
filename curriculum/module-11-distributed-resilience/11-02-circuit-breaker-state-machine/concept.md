# Circuit Breaker State Machine

When a downstream payment or search dependency goes brown (hanging 10s per request), blind retries exhaust your worker threads and cascade the outage upstream. A **Circuit Breaker** fast-fails immediately once a threshold is breached.

## Three States

1. **`CLOSED` (Normal):** Traffic flows through. Consecutive failures increment `failure_count`; any success resets `failure_count = 0`. When `failure_count >= failure_threshold`, transition to `OPEN` and record `opened_at = clock()`.
2. **`OPEN` (Fast-Fail):** Calls immediately raise `CircuitOpenError` without touching the upstream dependency. Once `clock() - opened_at >= recovery_timeout`, transition to `HALF_OPEN`.
3. **`HALF_OPEN` (Probe):** Allow at most `half_open_max_calls` trial call(s). If the probe succeeds, close the circuit (`CLOSED`, `failure_count = 0`). If the probe fails, trip immediately back to `OPEN` and reset `opened_at = clock()`.

## Injectable Monotonic Clock for Deterministic Testing

Never call `time.sleep()` inside unit tests. Inject `clock: Callable[[], float] = time.monotonic` so tests advance virtual time instantaneously:

```python
now = 100.0
gate = RateWindow(clock=lambda: now)
now += 31.0  # Instant simulated cooldown!
```
