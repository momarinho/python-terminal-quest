class FakeUserRepo:
    def __init__(self, emails: list[str] | None = None) -> None:
        self._emails = {e.strip().lower() for e in (emails or [])}

    def exists(self, email: str) -> bool:
        return email.strip().lower() in self._emails


class StubTokenGenerator:
    def __init__(self, fixed_token: str = "tok-fixed") -> None:
        self.fixed_token = fixed_token

    def next_token(self) -> str:
        return self.fixed_token


class SpyEmailSender:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, token: str) -> None:
        self.sent.append((to, token))
