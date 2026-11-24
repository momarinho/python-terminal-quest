## Concept: Warm-Up & Quick Syntax Reveal (Module 6)

Before building multi-module architecture and contract tests, practice the 3 essential **Pydantic v2** methods!

### Pattern Reveal #1 — Field Constraints (`Field(ge=1, le=65535)`)
```python
from pydantic import BaseModel, Field

class ServiceItem(BaseModel):
    name: str
    port: int = Field(ge=1, le=65535)
```

### Pattern Reveal #2 — Validating Untyped Dicts (`model_validate`)
```python
def validate_service(raw: dict[str, object]) -> ServiceItem:
    return ServiceItem.model_validate(raw)
```

### Pattern Reveal #3 — Serializing Back to a Dict (`model_dump`)
```python
def dump_service_dict(item: ServiceItem) -> dict[str, object]:
    return item.model_dump()
```

### Challenge
Open `warmup.py` and complete `ServiceItem`, `validate_service`, and `dump_service_dict`.
