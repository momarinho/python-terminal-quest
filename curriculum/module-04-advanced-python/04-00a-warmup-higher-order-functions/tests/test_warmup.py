from warmup import apply_twice, make_multiplier


def test_apply_twice() -> None:
    assert apply_twice(lambda n: n + 4, 10) == 18


def test_make_multiplier() -> None:
    triple = make_multiplier(3)
    assert triple(7) == 21
