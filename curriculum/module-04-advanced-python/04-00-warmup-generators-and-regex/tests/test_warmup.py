from warmup import apply_twice, extract_order_id, iter_even_numbers


def test_iter_even_numbers() -> None:
    assert list(iter_even_numbers(6)) == [0, 2, 4, 6]


def test_extract_order_id() -> None:
    assert extract_order_id("Payment settled for ORD-9042 yesterday") == "ORD-9042"
    assert extract_order_id("No order reference") is None


def test_apply_twice() -> None:
    assert apply_twice(lambda x: x + 3, 10) == 16
