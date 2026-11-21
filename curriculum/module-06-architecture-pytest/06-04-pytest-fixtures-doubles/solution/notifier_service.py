from typing import Protocol


class UserRepo(Protocol):
    def exists(self, email: str) -> bool: ...


class TokenGenerator(Protocol):
    def next_token(self) -> str: ...


class EmailSender(Protocol):
    def send(self, to: str, token: str) -> None: ...


class PasswordResetService:
    def __init__(
        self,
        users: UserRepo,
        tokens: TokenGenerator,
        mailer: EmailSender,
    ) -> None:
        self.users = users
        self.tokens = tokens
        self.mailer = mailer

    def request_reset(self, email: str) -> bool:
        """Issue and email a reset token iff user exists; return True if sent else False."""
        normalized = email.strip().lower()
        if not normalized or not self.users.exists(normalized):
            return False
        token = self.tokens.next_token()
        self.mailer.send(normalized, token)
        return True
