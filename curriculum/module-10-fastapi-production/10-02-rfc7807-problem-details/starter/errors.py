from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class DomainProblemError(Exception):
    status_code: int = 400
    error_type: str = "urn:problem:bad-request"
    title: str = "Bad Request"

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class NotFoundError(DomainProblemError):
    status_code = 404
    error_type = "urn:problem:not-found"
    title = "Resource Not Found"


class ConflictError(DomainProblemError):
    status_code = 409
    error_type = "urn:problem:conflict"
    title = "Conflict"


class ForbiddenError(DomainProblemError):
    status_code = 403
    error_type = "urn:problem:forbidden"
    title = "Forbidden"


def register_problem_handlers(app: FastAPI) -> None:
    """Register RFC 7807 problem+json handlers for DomainProblemError and RequestValidationError."""
    # TODO: add @app.exception_handler(DomainProblemError) and @app.exception_handler(RequestValidationError)
    _ = (app, Request, RequestValidationError, JSONResponse)
