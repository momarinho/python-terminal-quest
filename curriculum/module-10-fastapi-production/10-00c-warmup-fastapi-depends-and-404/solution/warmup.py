from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


def get_user_store() -> dict[str, str]:
    return {"alice": "admin"}


@app.get("/users/{username}")
def get_user(
    username: str,
    users: Annotated[dict[str, str], Depends(get_user_store)],
) -> dict[str, str]:
    role = users.get(username)
    if role is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "role": role}
