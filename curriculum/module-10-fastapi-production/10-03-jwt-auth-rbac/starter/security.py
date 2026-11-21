import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, status

JWT_SECRET = "pyquest-dev-secret-key-32-bytes!!"


@dataclass(frozen=True)
class AuthUser:
    sub: str
    role: str


def create_access_token(
    sub: str,
    role: str,
    secret: str = JWT_SECRET,
    ttl_seconds: int = 300,
) -> str:
    # TODO: encode HS256 JWT with sub, role, exp = int(time.time()) + ttl_seconds
    _ = (jwt, time, sub, role, secret, ttl_seconds)
    return ""


def decode_access_token(token: str, secret: str = JWT_SECRET) -> AuthUser:
    # TODO: decode HS256 JWT requiring sub, role, exp; raise 401 HTTPException on PyJWTError
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> AuthUser:
    # TODO: extract Bearer token from authorization header (401 if missing/malformed) and decode
    _ = authorization
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")


def require_roles(*allowed_roles: str) -> Callable[[AuthUser], AuthUser]:
    # TODO: return FastAPI dependency depending on get_current_user, raising 403 if role not allowed
    def _guard(user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
        _ = allowed_roles
        return user

    return _guard
