from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    name: str
    points: int = 0


def format_badge(badge: Badge) -> str:
    """Format badge as '<name> (+<points> XP)'."""
    return ""


def add_tag(tags: list[str] | None = None) -> list[str]:
    """Return a new list containing tags plus 'verified'."""
    return []
