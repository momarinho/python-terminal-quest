import pytest
from doubles import (
    FakeUserRepo,
    SpyEmailSender,
    StubTokenGenerator,
    verify_reset_service_contract,
)
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


def test_verify_reset_service_contract_catches_regressions() -> None:
    verify_reset_service_contract(PasswordResetService)

    class BuggyEmailsUnknown(PasswordResetService):
        def request_reset(self, email: str) -> bool:
            self.mailer.send(email.strip().lower(), self.tokens.next_token())
            return True

    class BuggySkipsNormalization(PasswordResetService):
        def request_reset(self, email: str) -> bool:
            if not email.strip() or not self.users.exists(email):
                return False
            self.mailer.send(email, self.tokens.next_token())
            return True

    class BuggySkipsSend(PasswordResetService):
        def request_reset(self, email: str) -> bool:
            normalized = email.strip().lower()
            return bool(normalized and self.users.exists(normalized))

    for buggy_cls in (BuggyEmailsUnknown, BuggySkipsNormalization, BuggySkipsSend):
        with pytest.raises(AssertionError):
            verify_reset_service_contract(buggy_cls)  # type: ignore[arg-type]
