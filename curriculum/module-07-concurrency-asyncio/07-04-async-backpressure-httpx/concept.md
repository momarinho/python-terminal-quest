## Concept: Async Backpressure (`asyncio.Semaphore`) & `httpx.AsyncClient`

Launching 5,000 `httpx` requests simultaneously without backpressure overwhelms file descriptors and downstream APIs. Wrap requests with `asyncio.Semaphore(limit)` so at most `limit` requests execute in flight at once!

### `httpx.AsyncClient` + `asyncio.Semaphore` + Injectable Sleep
```python
import asyncio
import httpx

async def fetch_package_meta(
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
    pkg: str,
) -> dict[str, object]:
    async with sem:
        resp = await client.get(f"https://registry.internal/{pkg}", timeout=2.0)
        resp.raise_for_status()
        return resp.json()
```

Passing `sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep` lets unit tests verify retry backoff counts without slowing down the test suite!

### Challenge
Implement `AsyncBatchFetcher` in `async_fetcher.py` using `asyncio.Semaphore(max_concurrency)`, bounded retries on `502`/`503`/`504` and `httpx.TimeoutException` (calling `await sleep_fn(base_delay * (2 ** attempt))`), and `fetch_all(paths)` returning parsed JSON payloads in order.
