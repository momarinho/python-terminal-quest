## Concept: Structured Concurrency (`asyncio.TaskGroup` & `asyncio.timeout`)

Classic `asyncio.create_task()` + `asyncio.gather()` can leave orphaned background tasks running if one task raises or times out. Python 3.11+ solves this with **structured concurrency**:

### `asyncio.TaskGroup` & `asyncio.timeout`
* `async with asyncio.TaskGroup() as tg:` waits for **all** spawned tasks to finish; if any task raises an unhandled error, `TaskGroup` automatically cancels sibling tasks and raises an `ExceptionGroup`.
* `async with asyncio.timeout(seconds):` cancels awaited work cleanly with `TimeoutError` when a deadline expires.
* Never call blocking `time.sleep(...)` inside an `async def` coroutine—use `await asyncio.sleep(...)` so the event loop stays responsive!

```python
import asyncio

async def poll_weather_stations(coros: list) -> list[str]:
    results: list[str] = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(c()) for c in coros]
    for task in tasks:
        results.append(task.result())
    return results
```

### Challenge
Implement `run_strict_taskgroup(task_fns, overall_timeout)` (cancelling on timeout or raising `ExceptionGroup` on failure) and `run_resilient_batch(task_fns, per_task_timeout)` (returning `{"ok": ..., "error": ...}` per task in input order without crashing sibling tasks on per-task failures/timeouts) in `async_orchestrator.py`.
