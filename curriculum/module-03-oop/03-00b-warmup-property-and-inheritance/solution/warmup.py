class Rectangle:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> int:
        """Return width * height."""
        return self.width * self.height


class UserBadge:
    def __init__(self, name: str) -> None:
        self.name = name

    def label(self) -> str:
        return self.name


class AdminBadge(UserBadge):
    """Subclass returning '[ADMIN] <name>'."""

    def label(self) -> str:
        return f"[ADMIN] {self.name}"
