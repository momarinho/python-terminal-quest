from warmup import iter_evens, iter_non_empty


def test_iter_evens() -> None:
    assert list(iter_evens(6)) == [0, 2, 4, 6]


def test_iter_non_empty() -> None:
    assert list(iter_non_empty([" ok ", "", "   ", "done"])) == ["ok", "done"]
