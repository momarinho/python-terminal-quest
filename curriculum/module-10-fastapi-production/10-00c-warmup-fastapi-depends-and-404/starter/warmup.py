from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException  # noqa: F401

app = FastAPI()


def get_user_store() -> dict[str, str]:
    return {"alice": "admin"}


@app.get("/users/{username}")
def get_user(
    username: str,
    users: Annotated[dict[str, str], Depends(get_user_store)],
) -> dict[str, str]:
    return {"username": username, "role": "missing"}
