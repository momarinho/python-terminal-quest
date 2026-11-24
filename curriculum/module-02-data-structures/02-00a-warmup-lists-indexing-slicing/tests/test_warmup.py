from warmup import first_and_last, last_three


def test_first_and_last() -> None:
    assert first_and_last(["alpha", "beta", "gamma"]) == ("alpha", "gamma")


def test_last_three() -> None:
    assert last_three([1, 2, 3, 4, 5]) == [3, 4, 5]
    assert last_three([9, 8]) == [9, 8]
