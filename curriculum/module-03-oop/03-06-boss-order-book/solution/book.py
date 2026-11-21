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
        if any(existing.order_id == order.order_id for existing in self._resting):
            raise ValueError(f"Duplicate active order_id: {order.order_id}")
        fills, next_resting, remainder = self._strategy.match(order, self._resting)
        if remainder is not None:
            next_resting.append(remainder)
        self._resting = next_resting
        return fills

    def cancel(self, order_id: str) -> bool:
        for idx, order in enumerate(self._resting):
            if order.order_id == order_id:
                del self._resting[idx]
                return True
        return False

    def best_bid(self) -> Decimal | None:
        bids = [o.price for o in self._resting if o.side == "BUY"]
        return max(bids) if bids else None

    def best_ask(self) -> Decimal | None:
        asks = [o.price for o in self._resting if o.side == "SELL"]
        return min(asks) if asks else None

    def __len__(self) -> int:
        return len(self._resting)

    def __iter__(self) -> Iterator[Order]:
        return iter(sorted(self._resting, key=lambda o: o.seq))
