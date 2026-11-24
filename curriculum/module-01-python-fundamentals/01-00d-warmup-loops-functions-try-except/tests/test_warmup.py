from warmup import parse_int_or_default, sum_positives


def test_sum_positives() -> None:
    assert sum_positives([-5, 3, 0, 7, -1]) == 10
    assert sum_positives([-2, -4]) == 0


def test_parse_int_or_default() -> None:
    assert parse_int_or_default(" 25 ") == 25
    assert parse_int_or_default("abc", default=9) == 9
