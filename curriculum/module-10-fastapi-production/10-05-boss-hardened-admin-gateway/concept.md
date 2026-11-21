## Boss Fight: Hardened Admin Gateway API

Wire together all production FastAPI pillars into a cohesive 4-file microservice.

### Multi-File Architecture (`security.py`, `errors.py`, `middleware.py`, `app.py`)
1. **`errors.py`**:
   * `GatewayProblemError` (`status_code`, `error_type`, `title`, `detail`) with `UnauthorizedError` (`401`), `ForbiddenError` (`403`), `NotFoundError` (`404`), and `ConflictError` (`409`).
   * `register_problem_handlers(app)` returning `application/problem+json` RFC 7807 responses (with `request_id` pulled from `REQUEST_ID_CTX` if set!) for `GatewayProblemError` AND `RequestValidationError` (`422`).
2. **`security.py`**:
   * `AuthUser(sub, role)`, `create_token(sub, role, ttl_seconds=300)`, `get_current_user` (raising `UnauthorizedError` on missing/bad/expired JWT), `require_roles(*roles)` (raising `ForbiddenError` on insufficient role).
3. **`middleware.py`**:
   * `REQUEST_ID_CTX: ContextVar[str | None]`, `install_request_context_middleware(app, audit_sink)`: propagates/generates `X-Request-ID`, echoes it in response headers, appends structured log dicts (`request_id`, `method`, `path`, `status_code`, `duration_ms`), and resets `ContextVar` in `finally:`.
4. **`app.py` -> `create_app(audit_sink=None) -> FastAPI`**:
   * `GET /health` -> `200 {"status": "ok"}` (unauthenticated).
   * `POST /admin/policies` (requires `"admin"` role, body `{"policy_id": str, "rate_limit": int > 0}`): returns `201`, raises `ConflictError` (`409`) on duplicate `policy_id`.
   * `GET /admin/policies/{policy_id}` (requires `"admin"` or `"auditor"` role): returns policy (`200`) or raises `NotFoundError` (`404`).
