import asyncio

import httpx
from aggregator import HealthAggregator
from client import ProbeClient


def test_cluster_health_aggregator_handles_retries_timeouts_and_degraded() -> None:
    flaky_calls = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal flaky_calls
        path = request.url.path
        if path == "/auth":
            flaky_calls += 1
            if flaky_calls == 1:
                return httpx.Response(503)
            return httpx.Response(200, json={"ok": True})
        if path == "/search":
            return httpx.Response(200, json={"ok": False})
        if path == "/slow":
            await asyncio.sleep(0.2)
            return httpx.Response(200, json={"ok": True})
        return httpx.Response(500)

    async def noop_sleep(_delay: float) -> None:
        return None

    async def run() -> dict[str, object]:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://cluster.local", transport=transport) as http:
            probe = ProbeClient(
                http,
                max_concurrency=2,
                per_probe_timeout=0.05,
                max_retries=1,
                sleep_fn=noop_sleep,
            )
            agg = HealthAggregator(probe)
            return await agg.check_cluster({
                "search": "/search",
                "auth": "/auth",
                "slow": "/slow",
            })

    summary = asyncio.run(run())
    assert summary["overall"] == "DEGRADED"
    assert summary["up_count"] == 1
    assert summary["down_count"] == 1
    services = {item["service"]: item for item in summary["services"]}  # type: ignore[attr-defined]
    assert services["auth"]["status"] == "UP"
    assert services["search"]["status"] == "DEGRADED"
    assert services["slow"]["status"] == "DOWN"
    assert services["slow"]["error"] == "timeout"


def test_cluster_all_down_reports_down() -> None:
    async def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    async def run() -> dict[str, object]:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://cluster.local", transport=transport) as http:
            agg = HealthAggregator(ProbeClient(http, max_retries=0))
            return await agg.check_cluster({"db": "/db"})

    summary = asyncio.run(run())
    assert summary["overall"] == "DOWN"
    assert summary["down_count"] == 1
