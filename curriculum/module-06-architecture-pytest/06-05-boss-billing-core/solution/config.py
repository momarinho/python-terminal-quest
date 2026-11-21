from decimal import Decimal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BillingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BILLING_", extra="ignore")

    gateway_secret: SecretStr
    tax_rate: Decimal = Field(default=Decimal("0.10"), ge=Decimal("0"), lt=Decimal("1"))

    @field_validator("gateway_secret")
    @classmethod
    def _require_secret(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("gateway_secret must not be empty")
        return value
