from dataclasses import FrozenInstanceError

import pytest
from warmup import Badge, add_tag, format_badge


def test_badge_frozen_and_default() -> None:
    b = Badge("Starter")
    assert b.points == 10
    with pytest.raises(FrozenInstanceError):
        b.points = 50  # type: ignore[misc]


def test_format_badge_and_add_tag() -> None:
    assert format_badge(Badge("Builder", 25)) == "Builder (+25 XP)"
    assert add_tag() == ["verified"]
    assert add_tag(["py"]) == ["py", "verified"]
