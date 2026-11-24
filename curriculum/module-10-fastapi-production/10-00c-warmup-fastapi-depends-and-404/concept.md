## Beginner Warm-Up 3: `Depends()` & `HTTPException(404)`

`Annotated[..., Depends(...)]` lets FastAPI inject services/config cleanly into routes—and tests swap them via `app.dependency_overrides`:

```python
from typing import Annotated

@app.get("/users/{username}")
def get_user(
    username: str,
    users: Annotated[dict[str, str], Depends(get_user_store)],
) -> dict[str, str]:
    role = users.get(username)
    if role is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "role": role}
```

### Challenge
Implement `get_user` in `warmup.py` using `Depends(get_user_store)` and raising `HTTPException(status_code=404, ...)`.
