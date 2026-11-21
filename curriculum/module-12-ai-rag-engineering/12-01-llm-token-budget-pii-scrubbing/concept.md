# LLM API Discipline — Token Budgeting & PII Scrubbing

Sending raw support transcripts straight to a commercial LLM API leaks customer PII and blows up context-window limits.

## 1. Zero-PII Pre-Flight Scrubbing

Scrub sensitive patterns **before** building the outgoing prompt payload or writing request logs:
- Email addresses -> `[EMAIL_REDACTED]`
- Government IDs (CPF `000.000.000-00` or SSN `000-00-0000`) -> `[GOV_ID_REDACTED]`
- HTTP `Bearer <token>` headers -> `Bearer [TOKEN_REDACTED]`
- Recognizable API keys (`sk-...`, `AIza...`, `ghp_...`) -> `[API_KEY_REDACTED]`

## 2. Deterministic Token-Budget Trimming

Always reserve tokens for:
1. The **system prompt** (anchor behavior & guardrails).
2. The **current user query** (what needs an answer right now).

Only fill the remaining token budget with **most-recent** conversation turns in chronological order, dropping the oldest turns first:

```python
import math

def approx_tokens(text: str) -> int:
    return math.ceil(len(text) / 4) if text else 0
```
