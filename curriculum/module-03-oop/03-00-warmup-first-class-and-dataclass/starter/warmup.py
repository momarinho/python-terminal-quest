from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    name: str
    points: int = 0  # Reveal: change default from 0 to 10


def format_badge(badge: Badge) -> str:
    """Format badge as '<name> (+<points> XP)'."""
    # Reveal: return f"{badge.name} (+{badge.points} XP)"
    return ""


def add_tag(tags: list[str] | None = None) -> list[str]:
    """Return a new list containing tags plus 'verified', safe against shared defaults."""
    # Reveal: result = list(tags) if tags is not None else []
    return []
