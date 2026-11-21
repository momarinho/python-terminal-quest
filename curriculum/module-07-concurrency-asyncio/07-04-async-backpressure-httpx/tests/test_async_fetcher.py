import asyncio

import httpx
import pytest
from async_fetcher import AsyncBatchFetcher, FetchClientError


def test_async_batch_fetcher_enforces_semaphore_and_retries() -> None:
    in_flight = 0
    peak_in_flight = 0
    attempts_by_path: dict[str, int] = {}
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal in_flight, peak_in_flight
        in_flight += 1
        peak_in_flight = max(peak_in_flight, in_flight)
        try:
            await asyncio.sleep(0.02)
            path = request.url.path
            attempts_by_path[path] = attempts_by_path.get(path, 0) + 1
            if path == "/flaky" and attempts_by_path[path] == 1:
                return httpx.Response(503)
            return httpx.Response(200, json={"path": path})
        finally:
            in_flight -= 1

    async def run() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://mock.local", transport=transport) as client:
            fetcher = AsyncBatchFetcher(
                client,
                max_concurrency=2,
                max_retries=2,
                base_delay=0.1,
                sleep_fn=fake_sleep,
            )
            results = await fetcher.fetch_all(["/a", "/flaky", "/b", "/c", "/d"])
            assert [r["path"] for r in results] == ["/a", "/flaky", "/b", "/c", "/d"]

    asyncio.run(run())
    assert peak_in_flight <= 2
    assert sleeps == [0.1]


def test_async_batch_fetcher_raises_on_404_and_timeout_exhaustion() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/timeout":
            raise httpx.ReadTimeout("timed out", request=request)
        return httpx.Response(404)

    async def noop_sleep(_delay: float) -> None:
        return None

    async def run() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://mock.local", transport=transport) as client:
            fetcher = AsyncBatchFetcher(client, max_retries=1, sleep_fn=noop_sleep)
            with pytest.raises(FetchClientError):
                await fetcher.fetch_one("/missing")
            with pytest.raises(FetchClientError):
                await fetcher.fetch_one("/timeout")

    asyncio.run(run())
