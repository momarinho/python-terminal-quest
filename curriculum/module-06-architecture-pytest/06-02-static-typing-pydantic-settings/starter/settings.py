from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SVC_", extra="ignore")

    service_name: str = "billing-api"
    api_token: SecretStr = SecretStr("TODO")
    timeout_sec: float = Field(default=5.0)
    max_retries: int = 2
    # TODO: require api_token (no insecure default), enforce timeout_sec > 0, max_retries >= 0, non-blank service_name
