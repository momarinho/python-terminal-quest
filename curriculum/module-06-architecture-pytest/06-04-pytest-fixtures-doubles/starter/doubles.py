from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notifier_service import PasswordResetService


class FakeUserRepo:
    def __init__(self, emails: list[str] | None = None) -> None:
        self._emails = {e.strip().lower() for e in (emails or [])}

    def exists(self, email: str) -> bool:
        return False


class StubTokenGenerator:
    def __init__(self, fixed_token: str = "tok-fixed") -> None:
        self.fixed_token = fixed_token

    def next_token(self) -> str:
        return ""


class SpyEmailSender:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, token: str) -> None:
        pass


def verify_reset_service_contract(service_cls: type[PasswordResetService]) -> None:
    """Assert that `service_cls` handles mixed-case existing users, unknown users, and blank emails."""
    _ = service_cls
