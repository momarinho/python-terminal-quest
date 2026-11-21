from decimal import Decimal

import pytest
from config import BillingSettings
from domain import Receipt
from pydantic import ValidationError
from service import BillingOrchestrator


class StubGateway:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Decimal, str]] = []

    def charge(self, account_id: str, total: Decimal, secret: str) -> str:
        self.calls.append((account_id, total, secret))
        return f"rcpt-{len(self.calls)}"


class FakeReceiptRepo:
    def __init__(self) -> None:
        self.items: dict[str, Receipt] = {}

    def save(self, receipt: Receipt) -> None:
        self.items[receipt.receipt_id] = receipt

    def get(self, receipt_id: str) -> Receipt | None:
        return self.items.get(receipt_id)


def test_billing_orchestrator_processes_subscription_and_usage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BILLING_GATEWAY_SECRET", "sk_live_abc")
    monkeypatch.setenv("BILLING_TAX_RATE", "0.10")
    settings = BillingSettings()  # type: ignore[call-arg]
    gw = StubGateway()
    repo = FakeReceiptRepo()
    orch = BillingOrchestrator(settings, gw, repo)

    sub_out = orch.process({
        "kind": "subscription",
        "account_id": " acct-1 ",
        "plan_price": "25.00",
        "seats": 3,
    })
    assert sub_out == {
        "receipt_id": "rcpt-1",
        "account_id": "acct-1",
        "subtotal": "75.00",
        "tax": "7.50",
        "total": "82.50",
    }
    assert gw.calls == [("acct-1", Decimal("82.50"), "sk_live_abc")]
    assert repo.get("rcpt-1") is not None


def test_billing_core_rejects_invalid_secret_or_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BILLING_GATEWAY_SECRET", "   ")
    with pytest.raises(ValidationError):
        BillingSettings()  # type: ignore[call-arg]

    monkeypatch.setenv("BILLING_GATEWAY_SECRET", "sk_test")
    orch = BillingOrchestrator(BillingSettings(), StubGateway(), FakeReceiptRepo())  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        orch.process({"kind": "usage", "account_id": "a1", "units": 0, "unit_price": "1.00"})
