from decimal import Decimal


class PolicyEvaluationError(Exception):
    """Raised when a payout policy or input fails validation."""


def resolve_fee_rate(policy: dict[str, object]) -> Decimal:
    """Resolve exact Decimal fee rate for a merchant policy using match/case."""
    # TODO: implement structural pattern matching for enterprise, growth, and starter tiers
    raise PolicyEvaluationError("Not implemented")
