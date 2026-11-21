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

    @app.exception_handler(DomainProblemError)
    async def handle_domain_problem(
        request: Request,
        exc: DomainProblemError,
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
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        cleaned_errors = [
            {
                "loc": list(err.get("loc", ())),
                "msg": str(err.get("msg", "")),
                "type": str(err.get("type", "")),
            }
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            media_type="application/problem+json",
            content={
                "type": "urn:problem:validation-error",
                "title": "Validation Failed",
                "status": 422,
                "detail": f"{len(cleaned_errors)} validation error(s) in request",
                "instance": request.url.path,
                "errors": cleaned_errors,
            },
        )
