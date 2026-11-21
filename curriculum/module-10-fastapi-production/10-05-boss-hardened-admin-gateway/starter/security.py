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
    # TODO: mint HS256 JWT with sub, role, exp
    _ = (jwt, time, sub, role, ttl_seconds)
    return ""


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> AuthUser:
    # TODO: validate Bearer token and raise UnauthorizedError on missing/invalid/expired JWT
    _ = authorization
    raise UnauthorizedError("Missing credentials")


def require_roles(*roles: str) -> Callable[[AuthUser], AuthUser]:
    def _guard(user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
        # TODO: raise ForbiddenError if user.role not in roles
        _ = (roles, ForbiddenError)
        return user

    return _guard
