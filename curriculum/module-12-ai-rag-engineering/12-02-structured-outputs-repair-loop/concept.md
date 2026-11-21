# Structured Outputs & Validation Repair Loop

Even when instructed to *"return JSON only"*, LLMs frequently wrap responses in markdown fences (` ```json ... ``` `), include commentary, or violate enum/type constraints (`"sev": "urgent"` instead of `"critical"`).

## Defensive Parsing + Bounded Repair

1. **Fence / Span Extraction:** Strip ` ```json ... ``` ` wrappers or extract the substring from the first `{` to the matching last `}`.
2. **Strict Schema Validation:** Parse directly via `TargetModel.model_validate_json(payload)` in Pydantic v2.
3. **Bounded Repair Loop:** When validation fails (`ValidationError` or `ValueError`), send a concise follow-up repair prompt quoting the exact Pydantic error back to the `LlmClient`, capped at `max_retries` so a broken model cannot loop forever.

```python
from pydantic import BaseModel, ValidationError

class AlertSummary(BaseModel):
    severity: str
    owner: str

def parse_alert(raw: str) -> AlertSummary:
    return AlertSummary.model_validate_json(raw)
```
