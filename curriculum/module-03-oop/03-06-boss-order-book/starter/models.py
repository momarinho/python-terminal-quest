from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True)
class Order:
    order_id: str
    side: Literal["BUY", "SELL"]
    price: Decimal
    qty: int
    seq: int = 0

    def __post_init__(self) -> None:
        # TODO: validate order_id, side in {'BUY', 'SELL'}, price > 0, qty > 0, seq >= 0
        pass

    def with_qty(self, new_qty: int) -> "Order":
        return replace(self, qty=new_qty)


@dataclass(frozen=True)
class TradeFill:
    buy_id: str
    sell_id: str
    price: Decimal
    qty: int
