from decimal import Decimal

import pytest
from events_schema import (
    CardChargeEvent,
    RefundEvent,
    parse_webhook,
    serialize_envelope,
)
from pydantic import ValidationError


def test_discriminated_union_parses_and_serializes_json_mode() -> None:
    env = parse_webhook({
        "event_id": " evt_100 ",
        "payload": {"kind": "card", "amount": "49.90", "last4": "4242"},
    })
    assert env.event_id == "evt_100"
    assert isinstance(env.payload, CardChargeEvent)
    assert env.payload.amount == Decimal("49.90")

    dumped = serialize_envelope(env)
    assert dumped == {
        "event_id": "evt_100",
        "payload": {"kind": "card", "amount": "49.90", "last4": "4242"},
    }


def test_validators_reject_bad_last4_and_partial_refund_without_reason() -> None:
    with pytest.raises(ValidationError):
        parse_webhook({"event_id": "e1", "payload": {"kind": "card", "amount": "10.00", "last4": "12ab"}})

    with pytest.raises(ValidationError):
        parse_webhook({"event_id": "e2", "payload": {"kind": "refund", "amount": "5.00", "partial": True}})

    full_refund = parse_webhook({"event_id": "e3", "payload": {"kind": "refund", "amount": "5.00", "partial": False}})
    assert isinstance(full_refund.payload, RefundEvent)
