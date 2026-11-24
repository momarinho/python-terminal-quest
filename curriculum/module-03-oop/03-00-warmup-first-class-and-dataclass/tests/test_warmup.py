from dataclasses import FrozenInstanceError

import pytest
from warmup import Badge, add_tag, format_badge


def test_badge_defaults_and_frozen() -> None:
    b = Badge(name="Pioneer")
    assert b.points == 10
    with pytest.raises(FrozenInstanceError):
        b.points = 99  # type: ignore[misc]


def test_format_badge() -> None:
    assert format_badge(Badge("Architect", 25)) == "Architect (+25 XP)"


def test_add_tag_avoids_shared_mutation() -> None:
    first = add_tag()
    second = add_tag(["core"])
    assert first == ["verified"]
    assert second == ["core", "verified"]
