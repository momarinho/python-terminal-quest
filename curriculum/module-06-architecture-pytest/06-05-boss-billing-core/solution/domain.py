from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator


class SubscriptionCharge(BaseModel):
    kind: Literal["subscription"]
    account_id: str = Field(min_length=1)
    plan_price: Decimal = Field(gt=Decimal("0"))
    seats: int = Field(ge=1)

    @field_validator("account_id")
    @classmethod
    def _clean_account(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("account_id must not be blank")
        return cleaned


class UsageCharge(BaseModel):
    kind: Literal["usage"]
    account_id: str = Field(min_length=1)
    units: int = Field(ge=1)
    unit_price: Decimal = Field(gt=Decimal("0"))

    @field_validator("account_id")
    @classmethod
    def _clean_account(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("account_id must not be blank")
        return cleaned


ChargeCommand = Annotated[SubscriptionCharge | UsageCharge, Field(discriminator="kind")]


class Receipt(BaseModel):
    receipt_id: str
    account_id: str
    subtotal: Decimal
    tax: Decimal
    total: Decimal
