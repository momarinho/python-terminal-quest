import asyncio
import time
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
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")
        self.client = client
        self.per_probe_timeout = per_probe_timeout
        self.max_retries = max(0, max_retries)
        self.sleep_fn = sleep_fn
        self._sem = asyncio.Semaphore(max_concurrency)

    async def probe(self, service: str, url: str) -> dict[str, object]:
        """Probe one service endpoint with semaphore + timeout + 503 retry, returning status dict."""
        attempts = self.max_retries + 1
        last_error = "unknown error"

        async with self._sem:
            for attempt in range(attempts):
                start = time.perf_counter()
                try:
                    async with asyncio.timeout(self.per_probe_timeout):
                        resp = await self.client.get(url)
                except (TimeoutError, httpx.TimeoutException):
                    last_error = "timeout"
                    if attempt + 1 < attempts:
                        await self.sleep_fn(0.02 * (attempt + 1))
                        continue
                    return {
                        "service": service,
                        "status": "DOWN",
                        "latency_ms": None,
                        "error": last_error,
                    }
                except httpx.HTTPError as exc:
                    return {
                        "service": service,
                        "status": "DOWN",
                        "latency_ms": None,
                        "error": str(exc),
                    }

                elapsed_ms = int((time.perf_counter() - start) * 1000)
                if resp.status_code == 503 and attempt + 1 < attempts:
                    last_error = "HTTP 503"
                    await self.sleep_fn(0.02 * (attempt + 1))
                    continue

                if resp.status_code != 200:
                    return {
                        "service": service,
                        "status": "DOWN",
                        "latency_ms": None,
                        "error": f"HTTP {resp.status_code}",
                    }

                try:
                    body = resp.json()
                except ValueError:
                    return {
                        "service": service,
                        "status": "DOWN",
                        "latency_ms": None,
                        "error": "invalid json",
                    }

                is_ok = bool(body.get("ok", True)) if isinstance(body, dict) else True
                return {
                    "service": service,
                    "status": "UP" if is_ok else "DEGRADED",
                    "latency_ms": elapsed_ms,
                    "error": None if is_ok else "dependency degraded",
                }

        return {"service": service, "status": "DOWN", "latency_ms": None, "error": last_error}
