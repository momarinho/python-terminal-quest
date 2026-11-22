## Concept: Static Typing Craft (`mypy`/`ruff`) & 12-Factor Config (`pydantic-settings`)

Production Python codebases combine **static verification** (`mypy --strict` / `pyright` for type soundness, `ruff check` + `ruff format` for lint/style) with **12-factor environment configuration** via `pydantic-settings`.

### `pydantic-settings` + `SecretStr`
Never read raw `os.environ["API_KEY"]` directly inside business logic or print secrets in logs! `SecretStr` masks values in `repr()`/`str()` while allowing explicit `.get_secret_value()` at the integration boundary.

```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class WeatherFeedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WEATHER_", extra="ignore")

    endpoint: str = "https://weather.internal"
    api_key: SecretStr
    timeout_sec: float = Field(default=3.0, gt=0.0)
```

### Modern Python 3.12/3.13 Typing (PEP 695, `Self`, `TypedDict`)
Modern Python removes `TypeVar` boilerplate with bracketed type parameters, `type` aliases, `typing.Self` for fluent builders, and `TypedDict` for structured dict contracts:
```python
from typing import Any, Self, TypedDict

type JsonMap = dict[str, Any]

def first[T](items: list[T]) -> T:
    return items[0]

class AuditHeaders(TypedDict):
    x_request_id: str
    x_actor: str

class QueryBuilder:
    def limit(self, n: int) -> Self:
        return self
```

### Challenge
Implement `AppSettings(BaseSettings)` in `settings.py` (with `env_prefix="SVC_"`, `SecretStr` `api_token`, `timeout_sec > 0`, `max_retries >= 0`) and `ClockProtocol` + `build_audit_header` in `contracts.py`.
