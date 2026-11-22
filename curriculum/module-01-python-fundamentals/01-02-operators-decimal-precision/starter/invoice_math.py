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

    # Replace this float math with exact Decimal arithmetic and .quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)
    subtotal = float(unit_price) * quantity
    discounted = subtotal * (1.0 - float(discount_pct) / 100.0)
    taxed = discounted * (1.0 + float(tax_pct) / 100.0)
    return Decimal(str(round(taxed, 2)))


def split_installments(total: Decimal, count: int) -> list[Decimal]:
    """Split total into `count` exact cent-balanced installments."""
    if count <= 0 or total < 0:
        raise ValueError("count must be positive and total non-negative")

    total_cents = int((total * _HUNDRED).to_integral_value(rounding=ROUND_HALF_UP))
    base_cents, remainder = divmod(total_cents, count)
    installments: list[Decimal] = []
    for idx in range(count):
        cents = base_cents + (1 if idx < remainder else 0)
        # Convert `cents` back to a 2-decimal-place Decimal (divide by _HUNDRED and quantize)
        installments.append(Decimal(cents))
    return installments
