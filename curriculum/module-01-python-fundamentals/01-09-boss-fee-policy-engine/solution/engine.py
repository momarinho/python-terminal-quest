from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from models import PolicyEvaluationError, resolve_fee_rate

_CENT = Decimal("0.01")


def evaluate_payout(
    merchant: str,
    amount_str: str,
    policy: dict[str, object],
    checks: list[bool],
    *,
    override_rate: Decimal | None = None,
) -> dict[str, object]:
    """Evaluate merchant payout fee and net settlement using exact Decimal math."""
    cleaned_merchant = merchant.strip()
    if not cleaned_merchant:
        raise PolicyEvaluationError("Merchant name must not be blank")

    try:
        amount = Decimal(amount_str).quantize(_CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise PolicyEvaluationError(f"Invalid payout amount: {amount_str!r}") from exc

    if amount <= 0:
        raise PolicyEvaluationError(f"Payout amount must be positive, got {amount}")

    if not checks or not all(checks):
        raise PolicyEvaluationError("Compliance gate failed")

    if override_rate is not None:
        if not (Decimal("0") <= override_rate < Decimal("1")):
            raise PolicyEvaluationError("override_rate must be in [0, 1)")
        rate = override_rate
    else:
        rate = resolve_fee_rate(policy)

    fee = (amount * rate).quantize(_CENT, rounding=ROUND_HALF_UP)
    net = amount - fee
    return {
        "merchant": cleaned_merchant,
        "gross": amount,
        "fee": fee,
        "net": net,
        "rate": rate,
    }


def format_payout_summary(result: dict[str, object]) -> str:
    """Format evaluated payout result into a fixed-width audit row."""
    merchant = str(result["merchant"])
    gross = result["gross"]
    fee = result["fee"]
    net = result["net"]
    return f"{merchant:<14} | gross={gross:>9.2f} | fee={fee:>7.2f} | net={net:>9.2f}"
