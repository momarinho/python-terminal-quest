from warmup import filter_min_amount, sum_by_category


def test_sum_by_category() -> None:
    rows = [
        {"category": "books", "amount": 30},
        {"category": "food", "amount": 20},
        {"category": "books", "amount": 15},
    ]
    assert sum_by_category(rows) == {"books": 45, "food": 20}


def test_filter_min_amount() -> None:
    rows: list[dict[str, int | str]] = [
        {"id": "a", "amount": 5},
        {"id": "b", "amount": 25},
    ]
    assert filter_min_amount(rows, 10) == [{"id": "b", "amount": 25}]
