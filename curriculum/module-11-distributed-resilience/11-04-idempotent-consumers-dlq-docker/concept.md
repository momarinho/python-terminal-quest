# Idempotent Consumers, DLQ & 12-Factor Container Hardening

## At-Least-Once Delivery Means Duplicate Events

Message brokers deliver **at least once**. Consumers must be idempotent by tracking processed `event_id` keys so duplicate deliveries are safely acknowledged as no-ops (`"DUPLICATE"`).

## Bounded Exponential Backoff + Dead-Letter Queue (DLQ)

When a message fails (`PoisonMessageError` or downstream outage):
- Retry with capped exponential backoff: `min(cap_seconds, base_seconds * (2 ** attempt_index))`.
- Once `attempts >= max_attempts`, **quarantine** the message into a Dead-Letter Queue (`dlq`) storing `{event_id, attempts, reason}` so one malformed event never blocks the entire partition.

## 12-Factor Container Hardening Checklist

Production Python containers should enforce:
1. **Multi-stage builds** (`uv sync --no-dev` in builder/runtime, zero build compilers in final slim image).
2. **Non-root UID** (`USER appuser`) so a container escape cannot modify system binaries.
3. **Config via environment** (`pydantic-settings` from `ENV`, zero secrets baked into layers).
4. **Healthchecks & Graceful `SIGTERM`**: orchestrators (Docker/Kubernetes) send `SIGTERM`; workers stop polling new jobs, finish the in-flight item, and flush DB connections before `SIGKILL`.

```python
import signal

class WorkerLoop:
    def __init__(self) -> None:
        self.stopping = False
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, "stopping", True))
```
