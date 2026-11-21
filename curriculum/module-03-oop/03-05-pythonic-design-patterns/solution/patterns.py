from decimal import ROUND_HALF_UP, Decimal
from typing import Protocol

_CENT = Decimal("0.01")


class PricingStrategy(Protocol):
    def apply(self, subtotal: Decimal) -> Decimal: ...


class NoDiscount:
    def apply(self, subtotal: Decimal) -> Decimal:
        return subtotal.quantize(_CENT, rounding=ROUND_HALF_UP)


class FlatDiscount:
    def __init__(self, amount: Decimal) -> None:
        if amount < 0:
            raise ValueError("Discount amount must be non-negative")
        self.amount = amount

    def apply(self, subtotal: Decimal) -> Decimal:
        return max(Decimal("0.00"), subtotal - self.amount).quantize(_CENT, rounding=ROUND_HALF_UP)


class PercentDiscount:
    def __init__(self, percent: Decimal) -> None:
        if not (Decimal("0") <= percent <= Decimal("100")):
            raise ValueError("Discount percent must be in [0, 100]")
        self.percent = percent

    def apply(self, subtotal: Decimal) -> Decimal:
        factor = Decimal("1") - (self.percent / Decimal("100"))
        return (subtotal * factor).quantize(_CENT, rounding=ROUND_HALF_UP)


def create_pricing_strategy(kind: str, value: str = "0") -> PricingStrategy:
    """Factory returning a PricingStrategy for 'none', 'flat', or 'percent'."""
    match kind.strip().lower():
        case "none":
            return NoDiscount()
        case "flat":
            return FlatDiscount(Decimal(value))
        case "percent":
            return PercentDiscount(Decimal(value))
        case _:
            raise ValueError(f"Unknown pricing strategy: {kind!r}")


class InvoiceRepository(Protocol):
    def save(self, invoice_id: str, record: dict[str, object]) -> None: ...
    def get(self, invoice_id: str) -> dict[str, object] | None: ...


class InMemoryInvoiceRepository:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, object]] = {}

    def save(self, invoice_id: str, record: dict[str, object]) -> None:
        self._store[invoice_id] = dict(record)

    def get(self, invoice_id: str) -> dict[str, object] | None:
        found = self._store.get(invoice_id)
        return dict(found) if found is not None else None
