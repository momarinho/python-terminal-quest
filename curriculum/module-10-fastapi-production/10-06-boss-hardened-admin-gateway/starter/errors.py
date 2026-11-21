from contextvars import ContextVar

from fastapi import FastAPI
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
    # TODO: register RFC 7807 handlers for GatewayProblemError and RequestValidationError
    _ = (app, RequestValidationError, JSONResponse, REQUEST_ID_CTX)
