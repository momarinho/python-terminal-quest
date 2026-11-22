## Concept: Pydantic v2 Boundary Validation & Discriminated Unions

Validating untrusted JSON at your service boundary with `Annotated[Union[...], Field(discriminator="kind")]` routes directly to the matching model in `O(1)`—producing crisp `ValidationError` diagnostics when fields are missing or malformed.

### Discriminated Unions & `model_validator`
```python
from typing import Annotated, Literal
from pydantic import BaseModel, Field, model_validator

class TempReading(BaseModel):
    kind: Literal["temp"]
    celsius: float = Field(ge=-100.0, le=200.0)

class DoorEvent(BaseModel):
    kind: Literal["door"]
    opened: bool
    reason: str | None = None

    @model_validator(mode="after")
    def _check_reason(self) -> "DoorEvent":
        if self.opened and not self.reason:
            raise ValueError("reason required when door opened")
        return self

SensorEvent = Annotated[TempReading | DoorEvent, Field(discriminator="kind")]
```

* Use `model.model_dump(mode="json")` when serializing `Decimal` or `datetime` fields into JSON-safe dictionaries.

### Challenge
Implement `CardChargeEvent`, `PixTransferEvent`, `RefundEvent`, `PaymentPayload` discriminated union, and `WebhookEnvelope` (with `event_id`, `payload`, `model_validator`, and `serialize_envelope`) in `events_schema.py`.
