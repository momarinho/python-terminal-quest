from warmup import AdminBadge, Rectangle, UserBadge


def test_rectangle_area_property() -> None:
    rect = Rectangle(4, 6)
    assert rect.area == 24


def test_admin_badge_inheritance() -> None:
    assert UserBadge("Ana").label() == "Ana"
    assert AdminBadge("Ana").label() == "[ADMIN] Ana"
