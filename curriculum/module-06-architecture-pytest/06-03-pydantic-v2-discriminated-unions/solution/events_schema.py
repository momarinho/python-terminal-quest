from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class CardChargeEvent(BaseModel):
    kind: Literal["card"]
    amount: Decimal = Field(gt=Decimal("0"))
    last4: str

    @field_validator("last4")
    @classmethod
    def _validate_last4(cls, value: str) -> str:
        if len(value) != 4 or not value.isdigit():
            raise ValueError("last4 must be exactly 4 digits")
        return value


class PixTransferEvent(BaseModel):
    kind: Literal["pix"]
    amount: Decimal = Field(gt=Decimal("0"))
    pix_key: str = Field(min_length=1)


class RefundEvent(BaseModel):
    kind: Literal["refund"]
    amount: Decimal = Field(gt=Decimal("0"))
    partial: bool = False
    reason: str | None = None

    @model_validator(mode="after")
    def _require_reason_for_partial(self) -> "RefundEvent":
        if self.partial and (not self.reason or not self.reason.strip()):
            raise ValueError("reason is required for partial refunds")
        return self


PaymentPayload = Annotated[
    CardChargeEvent | PixTransferEvent | RefundEvent,
    Field(discriminator="kind"),
]


class WebhookEnvelope(BaseModel):
    event_id: str = Field(min_length=1)
    payload: PaymentPayload

    @field_validator("event_id")
    @classmethod
    def _clean_event_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("event_id must not be blank")
        return cleaned


def parse_webhook(raw: dict[str, object]) -> WebhookEnvelope:
    return WebhookEnvelope.model_validate(raw)


def serialize_envelope(envelope: WebhookEnvelope) -> dict[str, object]:
    return envelope.model_dump(mode="json")
