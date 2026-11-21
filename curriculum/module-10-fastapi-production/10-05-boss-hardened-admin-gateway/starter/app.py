from errors import ConflictError, NotFoundError, register_problem_handlers
from fastapi import FastAPI
from middleware import install_request_context_middleware
from pydantic import BaseModel, Field
from security import AuthUser, require_roles


class PolicyCreate(BaseModel):
    policy_id: str = Field(min_length=1)
    rate_limit: int = Field(gt=0)


def create_app(audit_sink: list[dict[str, object]] | None = None) -> FastAPI:
    app = FastAPI(title="Hardened Admin Gateway")
    sink = audit_sink if audit_sink is not None else []
    register_problem_handlers(app)
    install_request_context_middleware(app, sink)
    policies: dict[str, dict[str, object]] = {}
    _ = (ConflictError, NotFoundError, AuthUser, require_roles, policies)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    # TODO: mount POST /admin/policies (role 'admin', status 201, 409 on dup)
    # and GET /admin/policies/{policy_id} (roles 'admin', 'auditor', 404 if missing)
    return app
