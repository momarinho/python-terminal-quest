import time
import uuid
from collections import Counter
from collections.abc import Awaitable, Callable
from contextvars import ContextVar

from fastapi import FastAPI, Request, Response

REQUEST_ID_CTX: ContextVar[str | None] = ContextVar("request_id", default=None)


class MetricsRegistry:
    def __init__(self) -> None:
        self.requests_total = 0
        self.errors_total = 0
        self.by_path: Counter[str] = Counter()

    def record(self, path: str, status_code: int) -> None:
        self.requests_total += 1
        if status_code >= 400:
            self.errors_total += 1
        self.by_path[path] += 1

    def snapshot(self) -> dict[str, object]:
        return {
            "requests_total": self.requests_total,
            "errors_total": self.errors_total,
            "by_path": dict(self.by_path),
        }


def install_observability(
    app: FastAPI,
    log_sink: list[dict[str, object]],
    metrics: MetricsRegistry,
) -> None:
    """Attach HTTP middleware for X-Request-ID propagation, ContextVar reset, JSON logs, and metrics."""

    @app.middleware("http")
    async def _correlation_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        req_id = (request.headers.get("X-Request-ID") or "").strip() or str(uuid.uuid4())
        token = REQUEST_ID_CTX.set(req_id)
        start = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = req_id
            return response
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 3)
            metrics.record(request.url.path, status_code)
            log_sink.append(
                {
                    "request_id": req_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                }
            )
            REQUEST_ID_CTX.reset(token)
