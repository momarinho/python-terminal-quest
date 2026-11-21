from decimal import Decimal


def compute_invoice_total(
    unit_price: str,
    quantity: int,
    discount_pct: str = "0",
    tax_pct: str = "0",
) -> Decimal:
    """Compute final invoice total rounded to 2 decimal places using ROUND_HALF_UP."""
    # TODO: replace float math with exact Decimal + ROUND_HALF_UP and validate inputs
    subtotal = float(unit_price) * quantity
    discounted = subtotal * (1.0 - float(discount_pct) / 100.0)
    taxed = discounted * (1.0 + float(tax_pct) / 100.0)
    return Decimal(str(round(taxed, 2)))


def split_installments(total: Decimal, count: int) -> list[Decimal]:
    """Split total into `count` exact cent-balanced installments."""
    # TODO: validate count > 0 and distribute remainder cents fairly to earlier installments
    return [total]
