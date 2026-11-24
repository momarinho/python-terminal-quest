from warmup import add_numbers, greet_player, split_bill_cents


def test_add_numbers() -> None:
    assert add_numbers(7, 5) == 12


def test_split_bill_cents() -> None:
    assert split_bill_cents(100, 3) == (33, 1)


def test_greet_player() -> None:
    assert greet_player("Alice", 1) == "Welcome, Alice! Level 1"
