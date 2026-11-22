from decimal import ROUND_HALF_UP, Decimal

_TWO_PLACES = Decimal("0.01")
_HUNDRED = Decimal("100")


def compute_invoice_total(
    unit_price: str,
    quantity: int,
    discount_pct: str = "0",
    tax_pct: str = "0",
) -> Decimal:
    """Compute final invoice total rounded to 2 decimal places using ROUND_HALF_UP."""
    if quantity < 0:
        raise ValueError("quantity must be non-negative")

    price = Decimal(unit_price)
    discount = Decimal(discount_pct)
    tax = Decimal(tax_pct)

    subtotal = price * quantity
    discounted = subtotal * (Decimal("1") - discount / _HUNDRED)
    taxed = discounted * (Decimal("1") + tax / _HUNDRED)
    return taxed.quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)


def split_installments(total: Decimal, count: int) -> list[Decimal]:
    """Split total into `count` exact cent-balanced installments."""
    if count <= 0 or total < 0:
        raise ValueError("count must be positive and total non-negative")

    total_cents = int((total * _HUNDRED).to_integral_value(rounding=ROUND_HALF_UP))
    base_cents, remainder = divmod(total_cents, count)
    installments: list[Decimal] = []
    for idx in range(count):
        cents = base_cents + (1 if idx < remainder else 0)
        installments.append((Decimal(cents) / _HUNDRED).quantize(_TWO_PLACES))
    return installments
