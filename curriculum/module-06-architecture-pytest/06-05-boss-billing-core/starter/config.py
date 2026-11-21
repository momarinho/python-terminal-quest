from decimal import Decimal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BillingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BILLING_", extra="ignore")

    gateway_secret: SecretStr = SecretStr("")
    tax_rate: Decimal = Field(default=Decimal("0.10"))
    # TODO: require non-empty gateway_secret and enforce 0 <= tax_rate < 1
