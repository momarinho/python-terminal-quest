from collections.abc import Iterator
from decimal import Decimal

from models import Order, TradeFill
from strategies import MatchingStrategy, PriceTimeStrategy


class OrderBook:
    """Composable limit OrderBook delegating execution to a MatchingStrategy."""

    def __init__(self, strategy: MatchingStrategy | None = None) -> None:
        self._strategy: MatchingStrategy = strategy or PriceTimeStrategy()
        self._resting: list[Order] = []

    def submit(self, order: Order) -> list[TradeFill]:
        # TODO: reject duplicate active order_id, invoke strategy.match, update _resting
        return []

    def cancel(self, order_id: str) -> bool:
        # TODO: remove resting order with matching order_id and return True if found
        return False

    def best_bid(self) -> Decimal | None:
        # TODO: highest resting BUY price or None
        return None

    def best_ask(self) -> Decimal | None:
        # TODO: lowest resting SELL price or None
        return None

    def __len__(self) -> int:
        return len(self._resting)

    def __iter__(self) -> Iterator[Order]:
        return iter(sorted(self._resting, key=lambda o: o.seq))
