import json


class SettlementError(Exception):
    """Base error for settlement decoding."""


class PayloadDecodeError(SettlementError):
    """Raised when raw JSON is malformed or not a JSON object."""


class InvalidAmountError(SettlementError):
    """Raised when amount_cents is missing or non-positive."""


def decode_settlement(raw_json: str, audit_log: list[str]) -> dict[str, object]:
    """Decode settlement payload, preserving exception cause and always recording cleanup."""
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise PayloadDecodeError("Invalid settlement JSON payload") from exc
    else:
        if not isinstance(parsed, dict):
            raise PayloadDecodeError("Settlement payload must be a JSON object")
        tx_id = parsed.get("tx_id")
        if not isinstance(tx_id, str) or not tx_id.strip():
            raise PayloadDecodeError("Missing valid tx_id")
        amount = parsed.get("amount_cents")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise InvalidAmountError(f"amount_cents must be a positive int, got {amount!r}")
        audit_log.append("OK")
        return {"tx_id": tx_id.strip(), "amount_cents": amount}
    finally:
        audit_log.append("RELEASED")
