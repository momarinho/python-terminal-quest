import asyncio
from collections.abc import Awaitable, Callable

import httpx


class FetchClientError(Exception):
    """Raised when an async HTTP fetch fails permanently or exhausts retries."""


class AsyncBatchFetcher:
    def __init__(
        self,
        client: httpx.AsyncClient,
        max_concurrency: int = 3,
        max_retries: int = 2,
        base_delay: float = 0.05,
        sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")
        self.client = client
        self.max_retries = max(0, max_retries)
        self.base_delay = base_delay
        self.sleep_fn = sleep_fn
        self._sem = asyncio.Semaphore(max_concurrency)

    async def fetch_one(self, path: str) -> dict[str, object]:
        # TODO: enforce semaphore backpressure + retry on TimeoutException or 502/503/504
        _ = path
        return {}

    async def fetch_all(self, paths: list[str]) -> list[dict[str, object]]:
        # TODO: fan out concurrently via TaskGroup and return results in order
        return []
