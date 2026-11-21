from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SVC_", extra="ignore")

    service_name: str = "billing-api"
    api_token: SecretStr
    timeout_sec: float = Field(default=5.0, gt=0.0)
    max_retries: int = Field(default=2, ge=0)

    @field_validator("service_name")
    @classmethod
    def _non_blank_service(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("service_name must not be blank")
        return cleaned

    @field_validator("api_token")
    @classmethod
    def _non_empty_token(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("api_token must not be empty")
        return value
