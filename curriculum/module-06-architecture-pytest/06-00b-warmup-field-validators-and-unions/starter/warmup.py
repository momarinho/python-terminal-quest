from typing import Literal

from pydantic import BaseModel, field_validator  # noqa: F401


class TagInput(BaseModel):
    tag: str

    # Add @field_validator("tag") to strip/lowercase and reject blank strings


class PingAction(BaseModel):
    kind: Literal["ping"]


class EmailAction(BaseModel):
    kind: Literal["email"]
    to: str


def format_action(event: PingAction | EmailAction) -> str:
    """Return 'pong' for PingAction or 'mail:<to>' for EmailAction."""
    return ""
