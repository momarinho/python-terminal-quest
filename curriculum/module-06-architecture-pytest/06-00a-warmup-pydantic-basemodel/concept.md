## Beginner Warm-Up 1: Pydantic v2 `BaseModel`

Pydantic validates untyped dicts/JSON automatically at runtime:

```python
from pydantic import BaseModel, Field

class ServiceItem(BaseModel):
    name: str
    port: int = Field(ge=1, le=65535)

def validate_service(raw: dict[str, object]) -> ServiceItem:
    return ServiceItem.model_validate(raw)
```

### Challenge
Complete `ServiceItem.port`, `validate_service`, and `dump_service_dict` in `warmup.py`.
