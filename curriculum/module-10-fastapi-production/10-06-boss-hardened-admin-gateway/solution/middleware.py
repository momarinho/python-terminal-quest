import time
import uuid
from collections.abc import Awaitable, Callable

from errors import REQUEST_ID_CTX
from fastapi import FastAPI, Request, Response


def install_request_context_middleware(
    app: FastAPI,
    audit_sink: list[dict[str, object]],
) -> None:
    @app.middleware("http")
    async def _gateway_middleware(
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
            audit_sink.append(
                {
                    "request_id": req_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": round((time.perf_counter() - start) * 1000, 3),
                }
            )
            REQUEST_ID_CTX.reset(token)
