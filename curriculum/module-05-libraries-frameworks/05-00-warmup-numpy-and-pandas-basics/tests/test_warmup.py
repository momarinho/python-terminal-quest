from warmup import filter_above_threshold, scale_array, total_column_sum


def test_scale_array() -> None:
    assert scale_array([1.0, 2.5, 4.0], 2.0) == [2.0, 5.0, 8.0]


def test_filter_above_threshold() -> None:
    assert filter_above_threshold([3, 10, 15, 2], 5) == [10, 15]


def test_total_column_sum() -> None:
    assert total_column_sum([{"qty": 4}, {"qty": 6}], "qty") == 10
    assert total_column_sum([], "qty") == 0
