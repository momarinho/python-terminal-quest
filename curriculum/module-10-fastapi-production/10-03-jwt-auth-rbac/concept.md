## Concept: JWT Authentication & RBAC (`401` vs. `403`)

Authentication and authorization return **distinct** HTTP status codes:
* **`401 Unauthorized`:** Missing, malformed, tampered, or expired credentials (*"Who are you?"*).
* **`403 Forbidden`:** Valid identity, insufficient permissions/role (*"I know who you are, and you can't access this"*).

### HS256 Tokens with `PyJWT` & Dependency Factories
```python
from datetime import UTC, datetime, timedelta
import jwt

def mint_token(user_id: str, role: str, secret: str, ttl_seconds: int = 300) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")
```

A parameterized RBAC factory `def require_roles(*allowed: str):` returns a FastAPI dependency that depends on `get_current_user` and raises `HTTPException(403)` if `user.role not in allowed`!

### Challenge
Implement `AuthUser`, `create_access_token`, `decode_access_token`, `get_current_user`, and `require_roles(*allowed_roles)` in `security.py`, and wire `/me` (any authenticated user) + `/admin/audit` (`admin` role only) in `app.py`.
