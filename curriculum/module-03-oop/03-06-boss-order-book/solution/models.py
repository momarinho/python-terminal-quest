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
        if not self.order_id.strip():
            raise ValueError("order_id must not be blank")
        if self.side not in {"BUY", "SELL"}:
            raise ValueError(f"Invalid side: {self.side!r}")
        if self.price <= 0:
            raise ValueError("price must be positive")
        if self.qty <= 0:
            raise ValueError("qty must be positive")
        if self.seq < 0:
            raise ValueError("seq must be non-negative")

    def with_qty(self, new_qty: int) -> "Order":
        return replace(self, qty=new_qty)


@dataclass(frozen=True)
class TradeFill:
    buy_id: str
    sell_id: str
    price: Decimal
    qty: int
