from warmup import double_positives, keep_recent, most_common_word


def test_double_positives() -> None:
    assert double_positives([-2, 0, 3, 5]) == [6, 10]


def test_most_common_word() -> None:
    assert most_common_word(["err", "ok", "err", "warn"]) == "err"


def test_keep_recent() -> None:
    assert keep_recent(["e1", "e2", "e3", "e4"], 2) == ["e3", "e4"]
