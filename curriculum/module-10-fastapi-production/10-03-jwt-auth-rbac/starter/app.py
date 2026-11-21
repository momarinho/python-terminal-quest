from typing import Annotated

from fastapi import Depends, FastAPI
from security import AuthUser, get_current_user, require_roles


def create_app() -> FastAPI:
    app = FastAPI(title="JWT RBAC Gateway")

    @app.get("/me")
    def read_me(user: Annotated[AuthUser, Depends(get_current_user)]) -> dict[str, str]:
        return {"sub": user.sub, "role": user.role}

    @app.get("/admin/audit")
    def read_admin_audit(
        user: Annotated[AuthUser, Depends(require_roles("admin"))],
    ) -> dict[str, object]:
        return {"audit": "ok", "actor": user.sub}

    return app
