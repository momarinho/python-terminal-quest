from typing import Annotated

from errors import REQUEST_ID_CTX, ConflictError, NotFoundError, register_problem_handlers
from fastapi import Depends, FastAPI, status
from middleware import install_request_context_middleware
from pydantic import BaseModel, Field, field_validator
from security import AuthUser, require_roles


class PolicyCreate(BaseModel):
    policy_id: str = Field(min_length=1)
    rate_limit: int = Field(gt=0)

    @field_validator("policy_id")
    @classmethod
    def _clean_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("policy_id must not be blank")
        return cleaned


def create_app(audit_sink: list[dict[str, object]] | None = None) -> FastAPI:
    app = FastAPI(title="Hardened Admin Gateway")
    sink = audit_sink if audit_sink is not None else []
    register_problem_handlers(app)
    install_request_context_middleware(app, sink)
    policies: dict[str, dict[str, object]] = {}

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/admin/policies", status_code=status.HTTP_201_CREATED)
    def create_policy(
        body: PolicyCreate,
        actor: Annotated[AuthUser, Depends(require_roles("admin"))],
    ) -> dict[str, object]:
        if body.policy_id in policies:
            raise ConflictError(f"Policy '{body.policy_id}' already exists")
        record: dict[str, object] = {
            "policy_id": body.policy_id,
            "rate_limit": body.rate_limit,
            "created_by": actor.sub,
            "request_id": REQUEST_ID_CTX.get(),
        }
        policies[body.policy_id] = record
        return record

    @app.get("/admin/policies/{policy_id}")
    def read_policy(
        policy_id: str,
        _actor: Annotated[AuthUser, Depends(require_roles("admin", "auditor"))],
    ) -> dict[str, object]:
        found = policies.get(policy_id)
        if found is None:
            raise NotFoundError(f"Policy '{policy_id}' not found")
        return found

    return app
