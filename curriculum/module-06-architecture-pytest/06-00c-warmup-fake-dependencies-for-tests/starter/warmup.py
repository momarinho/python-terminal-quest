from typing import Protocol


class Notifier(Protocol):
    def send(self, recipient: str, msg: str) -> None: ...


class MemoryNotifier:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, recipient: str, msg: str) -> None:
        """Record (recipient, msg) into self.sent."""
        pass


def welcome_user(email: str, notifier: Notifier) -> str:
    """Notify email with 'Welcome!' and return 'welcomed:<email>'."""
    return ""
