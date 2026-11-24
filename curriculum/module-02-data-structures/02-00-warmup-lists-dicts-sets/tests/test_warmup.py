from warmup import last_two, safe_lookup, square_positives


def test_last_two() -> None:
    assert last_two([10, 20, 30, 40]) == [30, 40]
    assert last_two([5]) == [5]


def test_square_positives() -> None:
    assert square_positives([-3, 0, 2, 4]) == [4, 16]


def test_safe_lookup() -> None:
    assert safe_lookup({"hits": 9}, "hits") == 9
    assert safe_lookup({"hits": 9}, "misses") == 0
