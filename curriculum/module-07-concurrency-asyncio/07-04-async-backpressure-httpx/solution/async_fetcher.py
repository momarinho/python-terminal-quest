import asyncio
from collections.abc import Awaitable, Callable

import httpx


class FetchClientError(Exception):
    """Raised when an async HTTP fetch fails permanently or exhausts retries."""


class AsyncBatchFetcher:
    _RETRYABLE = {502, 503, 504}

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
        attempts = self.max_retries + 1
        async with self._sem:
            for attempt in range(attempts):
                try:
                    resp = await self.client.get(path)
                except httpx.TimeoutException as exc:
                    if attempt + 1 < attempts:
                        await self.sleep_fn(self.base_delay * (2**attempt))
                        continue
                    raise FetchClientError(f"Timeout fetching {path}") from exc
                except httpx.HTTPError as exc:
                    raise FetchClientError(f"HTTP error fetching {path}: {exc}") from exc

                if resp.status_code in self._RETRYABLE and attempt + 1 < attempts:
                    await self.sleep_fn(self.base_delay * (2**attempt))
                    continue

                try:
                    resp.raise_for_status()
                    data = resp.json()
                except (httpx.HTTPStatusError, ValueError) as exc:
                    raise FetchClientError(f"Bad response {resp.status_code} for {path}") from exc

                if not isinstance(data, dict):
                    raise FetchClientError(f"Expected JSON object for {path}")
                return data

        raise FetchClientError(f"Exhausted retries for {path}")

    async def fetch_all(self, paths: list[str]) -> list[dict[str, object]]:
        if not paths:
            return []
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(self.fetch_one(p)) for p in paths]
        return [task.result() for task in tasks]
