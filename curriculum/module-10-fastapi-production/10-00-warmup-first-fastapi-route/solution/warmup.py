from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()


class EchoPayload(BaseModel):
    message: str


def get_app_version() -> str:
    return "1.0.0"


@app.get("/ping")
def ping(version: str = Depends(get_app_version)) -> dict[str, str]:
    """Return status 'pong' and injected version."""
    return {"status": "pong", "version": version}


@app.post("/echo", status_code=201)
def echo_item(payload: EchoPayload) -> dict[str, str]:
    """Echo back stripped message with HTTP 201 Created."""
    return {"echo": payload.message.strip()}
