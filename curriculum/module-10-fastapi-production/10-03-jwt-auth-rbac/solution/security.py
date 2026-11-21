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
    now = int(time.time())
    payload = {
        "sub": sub,
        "role": role,
        "iat": now,
        "exp": now + ttl_seconds,
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_access_token(token: str, secret: str = JWT_SECRET) -> AuthUser:
    try:
        claims = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"require": ["exp", "sub", "role"]},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    sub = claims.get("sub")
    role = claims.get("role")
    if not isinstance(sub, str) or not isinstance(role, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token claims",
        )
    return AuthUser(sub=sub, role=role)


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> AuthUser:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    parts = authorization.strip().split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expected Bearer token",
        )
    return decode_access_token(parts[1].strip())


def require_roles(*allowed_roles: str) -> Callable[[AuthUser], AuthUser]:
    allowed = set(allowed_roles)

    def _guard(user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' lacks permission",
            )
        return user

    return _guard
