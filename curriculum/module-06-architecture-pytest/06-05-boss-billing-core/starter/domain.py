from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class SubscriptionCharge(BaseModel):
    kind: Literal["subscription"]
    account_id: str
    plan_price: Decimal
    seats: int


class UsageCharge(BaseModel):
    kind: Literal["usage"]
    account_id: str
    units: int
    unit_price: Decimal


ChargeCommand = Annotated[SubscriptionCharge | UsageCharge, Field(discriminator="kind")]


class Receipt(BaseModel):
    receipt_id: str
    account_id: str
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    # TODO: add validation constraints (non-blank account_id, plan_price/unit_price > 0, seats/units >= 1)
