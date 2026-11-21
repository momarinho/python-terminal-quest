from decimal import ROUND_HALF_UP, Decimal
from typing import Protocol


class PricingStrategy(Protocol):
    def apply(self, subtotal: Decimal) -> Decimal: ...


class NoDiscount:
    def apply(self, subtotal: Decimal) -> Decimal:
        return subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class FlatDiscount:
    def __init__(self, amount: Decimal) -> None:
        if amount < 0:
            raise ValueError("Discount amount must be non-negative")
        self.amount = amount

    def apply(self, subtotal: Decimal) -> Decimal:
        # TODO: subtract self.amount, clamp at Decimal("0.00"), quantize to 0.01
        return subtotal


class PercentDiscount:
    def __init__(self, percent: Decimal) -> None:
        if not (Decimal("0") <= percent <= Decimal("100")):
            raise ValueError("Discount percent must be in [0, 100]")
        self.percent = percent

    def apply(self, subtotal: Decimal) -> Decimal:
        # TODO: apply percentage discount and quantize with ROUND_HALF_UP
        return subtotal


def create_pricing_strategy(kind: str, value: str = "0") -> PricingStrategy:
    """Factory returning a PricingStrategy for 'none', 'flat', or 'percent'."""
    # TODO: construct strategy or raise ValueError on unknown kind
    raise ValueError(f"Unknown strategy: {kind}")


class InvoiceRepository(Protocol):
    def save(self, invoice_id: str, record: dict[str, object]) -> None: ...
    def get(self, invoice_id: str) -> dict[str, object] | None: ...


class InMemoryInvoiceRepository:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, object]] = {}

    def save(self, invoice_id: str, record: dict[str, object]) -> None:
        # TODO: store copy of record
        pass

    def get(self, invoice_id: str) -> dict[str, object] | None:
        # TODO: retrieve record or None
        return None
