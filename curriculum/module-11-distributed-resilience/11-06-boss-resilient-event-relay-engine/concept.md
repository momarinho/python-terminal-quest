# Boss Fight — Resilient Event Relay Engine

Assemble all four distributed resilience primitives into one cohesive multi-file service:

- **`idempotency.py`**: Canonical SHA-256 request fingerprinting (`IdempotencyConflictError` on key mismatch, cached `(event_id, replayed=True)` on matching retries).
- **`outbox.py`**: SQLite `outbox_events` persistence (`PENDING` -> `PUBLISHED` or `DEAD_LETTER`) with `attempts` and `last_error`.
- **`breaker.py`**: Injectable-clock `CircuitBreaker` (`CLOSED` -> `OPEN` -> `HALF_OPEN`) protecting webhook/broker dispatch.
- **`engine.py`**: `ResilientRelayEngine` exposing:
  1. `submit_command(idempotency_key: str, event_type: str, payload: dict[str, object]) -> SubmitResult` — enforces idempotency and queues a `PENDING` outbox event atomically.
  2. `dispatch_pending(limit: int = 50) -> DispatchReport` — relays `PENDING` events through the `CircuitBreaker`:
     - On success -> mark `PUBLISHED`.
     - If `CircuitOpenError` -> leave `PENDING` without consuming retry budget (broker wasn't even called!).
     - On upstream exception -> increment `attempts`; mark `DEAD_LETTER` once `attempts >= max_attempts`, else keep `PENDING`.

## Design Invariant

When the Circuit Breaker fast-fails (`CircuitOpenError`), **do not** burn an event's DLQ retry attempts! Cooldown pauses delivery cleanly without falsely poisoning healthy events.
