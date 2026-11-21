import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

import jwt
from errors import ForbiddenError, UnauthorizedError
from fastapi import Depends, Header

GATEWAY_SECRET = "pyquest-gateway-secret-32bytes!"


@dataclass(frozen=True)
class AuthUser:
    sub: str
    role: str


def create_token(sub: str, role: str, ttl_seconds: int = 300) -> str:
    now = int(time.time())
    return jwt.encode(
        {"sub": sub, "role": role, "iat": now, "exp": now + ttl_seconds},
        GATEWAY_SECRET,
        algorithm="HS256",
    )


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> AuthUser:
    if not authorization:
        raise UnauthorizedError("Missing Authorization header")
    parts = authorization.strip().split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise UnauthorizedError("Expected Bearer token")

    try:
        claims = jwt.decode(
            parts[1].strip(),
            GATEWAY_SECRET,
            algorithms=["HS256"],
            options={"require": ["exp", "sub", "role"]},
        )
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Invalid or expired JWT") from exc

    sub = claims.get("sub")
    role = claims.get("role")
    if not isinstance(sub, str) or not isinstance(role, str):
        raise UnauthorizedError("Malformed JWT claims")
    return AuthUser(sub=sub, role=role)


def require_roles(*roles: str) -> Callable[[AuthUser], AuthUser]:
    allowed = set(roles)

    def _guard(user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
        if user.role not in allowed:
            raise ForbiddenError(f"Role '{user.role}' is not permitted")
        return user

    return _guard
