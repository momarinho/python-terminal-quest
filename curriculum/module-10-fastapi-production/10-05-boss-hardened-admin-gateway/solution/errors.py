from contextvars import ContextVar

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

REQUEST_ID_CTX: ContextVar[str | None] = ContextVar("gateway_request_id", default=None)


class GatewayProblemError(Exception):
    status_code: int = 400
    error_type: str = "urn:gateway:bad-request"
    title: str = "Bad Request"

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class UnauthorizedError(GatewayProblemError):
    status_code = 401
    error_type = "urn:gateway:unauthorized"
    title = "Unauthorized"


class ForbiddenError(GatewayProblemError):
    status_code = 403
    error_type = "urn:gateway:forbidden"
    title = "Forbidden"


class NotFoundError(GatewayProblemError):
    status_code = 404
    error_type = "urn:gateway:not-found"
    title = "Not Found"


class ConflictError(GatewayProblemError):
    status_code = 409
    error_type = "urn:gateway:conflict"
    title = "Conflict"


def register_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(GatewayProblemError)
    async def handle_gateway_problem(
        request: Request,
        exc: GatewayProblemError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            media_type="application/problem+json",
            content={
                "type": exc.error_type,
                "title": exc.title,
                "status": exc.status_code,
                "detail": exc.detail,
                "instance": request.url.path,
                "request_id": REQUEST_ID_CTX.get(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        errors = [
            {"loc": list(e.get("loc", ())), "msg": str(e.get("msg", "")), "type": str(e.get("type", ""))}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            media_type="application/problem+json",
            content={
                "type": "urn:gateway:validation-error",
                "title": "Validation Failed",
                "status": 422,
                "detail": f"{len(errors)} validation error(s)",
                "instance": request.url.path,
                "request_id": REQUEST_ID_CTX.get(),
                "errors": errors,
            },
        )
