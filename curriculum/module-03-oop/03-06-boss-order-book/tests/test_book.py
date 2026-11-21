from decimal import Decimal

import pytest
from book import OrderBook
from models import Order, TradeFill
from strategies import ImmediateOrCancelStrategy


def test_price_time_matching_partial_fill_and_dunders() -> None:
    book = OrderBook()
    book.submit(Order("s1", "SELL", Decimal("101.00"), 5, seq=1))
    book.submit(Order("s2", "SELL", Decimal("100.00"), 4, seq=2))
    assert book.best_ask() == Decimal("100.00")

    fills = book.submit(Order("b1", "BUY", Decimal("101.00"), 6, seq=3))
    assert fills == [
        TradeFill("b1", "s2", Decimal("100.00"), 4),
        TradeFill("b1", "s1", Decimal("101.00"), 2),
    ]
    assert len(book) == 1
    resting_orders = list(book)
    assert resting_orders[0].order_id == "s1"
    assert resting_orders[0].qty == 3
    assert book.cancel("s1") is True
    assert len(book) == 0


def test_ioc_strategy_never_rests_remainder_and_validates_duplicates() -> None:
    book = OrderBook(strategy=ImmediateOrCancelStrategy())
    # Resting order won't rest under IOC, so switch or test IOC incoming against empty book
    fills = book.submit(Order("b-ioc", "BUY", Decimal("50.00"), 10, seq=1))
    assert fills == []
    assert len(book) == 0

    pt_book = OrderBook()
    pt_book.submit(Order("b1", "BUY", Decimal("50.00"), 5, seq=1))
    with pytest.raises(ValueError):
        pt_book.submit(Order("b1", "BUY", Decimal("51.00"), 2, seq=2))
