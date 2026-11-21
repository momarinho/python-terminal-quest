import asyncio
from collections.abc import Awaitable, Callable

import httpx


class ProbeClient:
    def __init__(
        self,
        client: httpx.AsyncClient,
        max_concurrency: int = 4,
        per_probe_timeout: float = 0.5,
        max_retries: int = 1,
        sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        self.client = client
        self.per_probe_timeout = per_probe_timeout
        self.max_retries = max(0, max_retries)
        self.sleep_fn = sleep_fn
        self._sem = asyncio.Semaphore(max_concurrency)

    async def probe(self, service: str, url: str) -> dict[str, object]:
        """Probe one service endpoint with semaphore + timeout + 503 retry, returning status dict."""
        # TODO: return {'service': service, 'status': 'UP'|'DEGRADED'|'DOWN', 'latency_ms': int|None, 'error': str|None}
        _ = (url, httpx)
        return {"service": service, "status": "DOWN", "latency_ms": None, "error": "not implemented"}
