import time
import uuid
from collections import Counter
from contextvars import ContextVar

from fastapi import FastAPI, Request, Response

REQUEST_ID_CTX: ContextVar[str | None] = ContextVar("request_id", default=None)


class MetricsRegistry:
    def __init__(self) -> None:
        self.requests_total = 0
        self.errors_total = 0
        self.by_path: Counter[str] = Counter()

    def record(self, path: str, status_code: int) -> None:
        # TODO: increment requests_total, errors_total if >= 400, and by_path[path]
        _ = (path, status_code)

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
    # TODO: attach @app.middleware("http") handler
    _ = (app, log_sink, metrics, Request, Response, time, uuid)
