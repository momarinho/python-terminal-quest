import json


class SettlementError(Exception):
    """Base error for settlement decoding."""


class PayloadDecodeError(SettlementError):
    """Raised when raw JSON is malformed or not a JSON object."""


class InvalidAmountError(SettlementError):
    """Raised when amount_cents is missing or non-positive."""


def decode_settlement(raw_json: str, audit_log: list[str]) -> dict[str, object]:
    """Decode settlement payload, preserving exception cause and always recording cleanup."""
    # TODO: use try/except (raise ... from exc)/else/finally
    return json.loads(raw_json)
