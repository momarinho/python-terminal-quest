## Concept: RFC 7807 `ProblemDetail` Error Contracts in FastAPI

Returning inconsistent error JSON shapes (`{"msg": ...}` vs `{"detail": [...]}`) forces API clients to write brittle error parsers. **RFC 7807** (`application/problem+json`) standardizes every HTTP error around:
* `type` (URI identifying the error class, e.g. `"urn:problem:not-found"`)
* `title` (short human summary)
* `status` (HTTP status code)
* `detail` (instance-specific message)
* `instance` (`request.url.path`)
* optional `errors` (structured field validation errors on `422`)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

@app.exception_handler(ItemMissingError)
async def handle_missing(request: Request, exc: ItemMissingError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        media_type="application/problem+json",
        content={
            "type": "urn:problem:item-missing",
            "title": "Resource Not Found",
            "status": 404,
            "detail": str(exc),
            "instance": request.url.path,
        },
    )
```

### Challenge
Implement `DomainProblemError`, `NotFoundError`, `ConflictError`, `ForbiddenError`, and `register_problem_handlers(app)` in `errors.py` (covering domain exceptions AND `RequestValidationError` -> `422` with `errors` list), and wire the `/orders` routes in `app.py`.
