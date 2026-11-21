from decimal import Decimal, InvalidOperation

import pytest
from engine import evaluate_payout, format_payout_summary
from models import PolicyEvaluationError, resolve_fee_rate


def test_enterprise_and_growth_policy_routing() -> None:
    assert resolve_fee_rate({"tier": "enterprise", "monthly_volume": 150_000}) == Decimal("0.0125")
    assert resolve_fee_rate({"tier": "enterprise", "monthly_volume": 10_000}) == Decimal("0.0175")
    assert resolve_fee_rate({"tier": "growth", "high_risk": True}) == Decimal("0.0350")
    assert resolve_fee_rate({"tier": "growth", "high_risk": False}) == Decimal("0.0250")
    assert resolve_fee_rate({"tier": "starter"}) == Decimal("0.0290")


def test_evaluate_payout_precision_and_summary() -> None:
    res = evaluate_payout(
        "  acme-pay ",
        "1000.00",
        {"tier": "enterprise", "monthly_volume": 200_000},
        [True, True],
    )
    assert res["fee"] == Decimal("12.50")
    assert res["net"] == Decimal("987.50")
    assert format_payout_summary(res) == "acme-pay       | gross=  1000.00 | fee=  12.50 | net=   987.50"


def test_override_rate_is_keyword_only_and_chaining_works() -> None:
    res = evaluate_payout("beta", "100.00", {"tier": "starter"}, [True], override_rate=Decimal("0.05"))
    assert res["fee"] == Decimal("5.00")

    with pytest.raises(PolicyEvaluationError) as exc_info:
        evaluate_payout("beta", "not-a-number", {"tier": "starter"}, [True])
    assert isinstance(exc_info.value.__cause__, InvalidOperation)

    with pytest.raises(PolicyEvaluationError):
        evaluate_payout("beta", "100.00", {"tier": "starter"}, [])
    with pytest.raises(PolicyEvaluationError):
        evaluate_payout("beta", "100.00", {"tier": "unknown"}, [True])
