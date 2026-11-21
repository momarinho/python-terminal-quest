from decimal import Decimal

import pytest
from patterns import InMemoryInvoiceRepository, create_pricing_strategy
from service import BillingService


def test_strategy_factory_and_clamping() -> None:
    flat = create_pricing_strategy("flat", "25.00")
    assert flat.apply(Decimal("10.00")) == Decimal("0.00")

    pct = create_pricing_strategy("percent", "15")
    assert pct.apply(Decimal("200.00")) == Decimal("170.00")

    with pytest.raises(ValueError):
        create_pricing_strategy("bogo", "10")


def test_billing_service_persists_via_repository_protocol() -> None:
    repo = InMemoryInvoiceRepository()
    svc = BillingService(repo)
    inv = svc.create_invoice("inv-101", Decimal("100.00"), "percent", "20")
    assert inv["total"] == Decimal("80.00")
    assert repo.get("inv-101") == {
        "id": "inv-101",
        "subtotal": Decimal("100.00"),
        "total": Decimal("80.00"),
    }
