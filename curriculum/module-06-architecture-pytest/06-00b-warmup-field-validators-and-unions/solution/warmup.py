from typing import Literal

from pydantic import BaseModel, field_validator


class TagInput(BaseModel):
    tag: str

    @field_validator("tag")
    @classmethod
    def clean_tag(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("tag cannot be blank")
        return cleaned


class PingAction(BaseModel):
    kind: Literal["ping"]


class EmailAction(BaseModel):
    kind: Literal["email"]
    to: str


def format_action(event: PingAction | EmailAction) -> str:
    """Return 'pong' for PingAction or 'mail:<to>' for EmailAction."""
    if event.kind == "ping":
        return "pong"
    return f"mail:{event.to}"
