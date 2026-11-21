from decimal import Decimal

import pytest
from invoice_math import compute_invoice_total, split_installments


def test_avoids_ieee754_drift_and_uses_half_up() -> None:
    # 0.10 * 3 = 0.30 exact (float would produce 0.30000000000000004)
    assert compute_invoice_total("0.10", 3) == Decimal("0.30")
    # 10.05 * 1 * 1.05 = 10.5525 -> 10.55; 10.05 * 1 * 1.055 = 10.60275 -> 10.60
    # 10.00 * 1 with 1.055% tax -> 10.1055 -> 10.11; exact half-cent: 0.01 * 1 with 50% tax = 0.015 -> 0.02
    assert compute_invoice_total("0.01", 1, tax_pct="50") == Decimal("0.02")


def test_discount_then_tax() -> None:
    total = compute_invoice_total("100.00", 2, discount_pct="15", tax_pct="10")
    assert total == Decimal("187.00")


def test_split_installments_preserves_exact_total() -> None:
    parts = split_installments(Decimal("10.00"), 3)
    assert parts == [Decimal("3.34"), Decimal("3.33"), Decimal("3.33")]
    assert sum(parts) == Decimal("10.00")


def test_invalid_inputs_raise_value_error() -> None:
    with pytest.raises(ValueError):
        compute_invoice_total("10.00", -1)
    with pytest.raises(ValueError):
        split_installments(Decimal("10.00"), 0)
