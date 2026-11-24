from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    name: str
    points: int = 10


def format_badge(badge: Badge) -> str:
    """Format badge as '<name> (+<points> XP)'."""
    return f"{badge.name} (+{badge.points} XP)"


def add_tag(tags: list[str] | None = None) -> list[str]:
    """Return a new list containing tags plus 'verified'."""
    result = list(tags) if tags is not None else []
    result.append("verified")
    return result
