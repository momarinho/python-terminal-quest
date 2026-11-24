import pytest
from pydantic import ValidationError
from warmup import EmailAction, PingAction, TagInput, format_action


def test_tag_input_validator() -> None:
    assert TagInput(tag="  FastAPI ").tag == "fastapi"
    with pytest.raises(ValidationError):
        TagInput(tag="   ")


def test_format_action() -> None:
    assert format_action(PingAction(kind="ping")) == "pong"
    assert format_action(EmailAction(kind="email", to="dev@example.com")) == "mail:dev@example.com"
