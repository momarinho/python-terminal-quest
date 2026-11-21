from decimal import Decimal


class PolicyEvaluationError(Exception):
    """Raised when a payout policy or input fails validation."""


def resolve_fee_rate(policy: dict[str, object]) -> Decimal:
    """Resolve exact Decimal fee rate for a merchant policy using match/case."""
    match policy:
        case {"tier": "enterprise", "monthly_volume": int(vol)} if (
            not isinstance(vol, bool) and vol >= 100_000
        ):
            return Decimal("0.0125")
        case {"tier": "enterprise"}:
            return Decimal("0.0175")
        case {"tier": "growth", "high_risk": True}:
            return Decimal("0.0350")
        case {"tier": "growth"}:
            return Decimal("0.0250")
        case {"tier": "starter"}:
            return Decimal("0.0290")
        case _:
            raise PolicyEvaluationError(f"Unsupported merchant policy: {policy!r}")
