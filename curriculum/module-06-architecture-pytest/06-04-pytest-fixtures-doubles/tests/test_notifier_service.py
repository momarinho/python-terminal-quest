import pytest
from doubles import FakeUserRepo, SpyEmailSender, StubTokenGenerator
from notifier_service import PasswordResetService


@pytest.fixture
def reset_harness() -> tuple[PasswordResetService, SpyEmailSender]:
    repo = FakeUserRepo(["ana@acme.dev"])
    tokens = StubTokenGenerator("reset-999")
    spy = SpyEmailSender()
    return PasswordResetService(repo, tokens, spy), spy


@pytest.mark.parametrize(
    ("raw_email", "expected_sent"),
    [
        ("  ANA@acme.dev ", True),
        ("ghost@acme.dev", False),
        ("   ", False),
    ],
)
def test_request_reset_with_fixtures_and_doubles(
    reset_harness: tuple[PasswordResetService, SpyEmailSender],
    raw_email: str,
    expected_sent: bool,
) -> None:
    svc, spy = reset_harness
    assert svc.request_reset(raw_email) is expected_sent
    if expected_sent:
        assert spy.sent == [("ana@acme.dev", "reset-999")]
    else:
        assert spy.sent == []
