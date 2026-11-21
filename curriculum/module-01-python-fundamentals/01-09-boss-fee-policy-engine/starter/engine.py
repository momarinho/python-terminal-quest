from decimal import Decimal

from models import PolicyEvaluationError, resolve_fee_rate


def evaluate_payout(
    merchant: str,
    amount_str: str,
    policy: dict[str, object],
    checks: list[bool],
    *,
    override_rate: Decimal | None = None,
) -> dict[str, object]:
    """Evaluate merchant payout fee and net settlement using exact Decimal math."""
    # TODO: validate merchant, parse Decimal amount_str (chaining InvalidOperation),
    # enforce non-empty all(checks), resolve rate (or override_rate), and compute fee/net.
    _ = (PolicyEvaluationError, resolve_fee_rate, override_rate)
    return {}


def format_payout_summary(result: dict[str, object]) -> str:
    """Format evaluated payout result into a fixed-width audit row."""
    # TODO: '<merchant:<14> | gross=<gross:>9.2f> | fee=<fee:>7.2f> | net=<net:>9.2f>'
    return ""
