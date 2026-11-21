from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class CardChargeEvent(BaseModel):
    kind: Literal["card"]
    amount: Decimal
    last4: str


class PixTransferEvent(BaseModel):
    kind: Literal["pix"]
    amount: Decimal
    pix_key: str


class RefundEvent(BaseModel):
    kind: Literal["refund"]
    amount: Decimal
    partial: bool = False
    reason: str | None = None


PaymentPayload = Annotated[
    CardChargeEvent | PixTransferEvent | RefundEvent,
    Field(discriminator="kind"),
]


class WebhookEnvelope(BaseModel):
    event_id: str
    payload: PaymentPayload
    # TODO: enforce non-empty event_id, positive amount, 4-digit last4, and reason required when RefundEvent.partial is True


def parse_webhook(raw: dict[str, object]) -> WebhookEnvelope:
    return WebhookEnvelope.model_validate(raw)


def serialize_envelope(envelope: WebhookEnvelope) -> dict[str, object]:
    # TODO: return JSON-safe dict via model_dump(mode="json")
    return {}
