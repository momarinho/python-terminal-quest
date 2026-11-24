from warmup import average_or_zero, scale_values


def test_scale_values() -> None:
    assert scale_values([1.5, 2.0, 4.0], 2.0) == [3.0, 4.0, 8.0]


def test_average_or_zero() -> None:
    assert average_or_zero([10.0, 20.0, 30.0]) == 20.0
    assert average_or_zero([]) == 0.0
