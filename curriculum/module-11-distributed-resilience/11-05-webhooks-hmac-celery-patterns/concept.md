# Webhook HMAC-SHA256 Security & Celery Worker Patterns

## 1. Webhook Signature + Replay-Window Verification (`webhook.py`)

Public webhook endpoints (Stripe, GitHub, Mercado Pago) sign `f"{timestamp}.{raw_body}"` with a shared secret:
1. Validate timestamp freshness (`abs(clock() - ts) <= max_age_seconds`) so captured old requests cannot be replayed hours later.
2. Compute `hmac.new(secret, signed_bytes, hashlib.sha256).hexdigest()` and verify with constant-time **`hmac.compare_digest`** (never `==`, which leaks byte timing!).
3. Parse `raw_body` **verbatim** before JSON serialization—re-serializing JSON alters whitespace/key order and breaks signatures.

## 2. Celery + Redis/RabbitMQ Worker Topology (`worker.py`) & ASGI Sizing

In production Celery architectures:
- **Broker (Redis / RabbitMQ):** Holds queued task messages until delivered.
- **Result Backend (Redis / Postgres):** Persists task state transitions (`PENDING` -> `RETRY` -> `SUCCESS` / `FAILURE`).
- **`acks_late = True`:** Only acknowledge the broker message *after* task execution finishes—combined with **idempotent** task logic, if a worker crashes mid-job (`SIGKILL`), another worker re-runs the message safely without silent drops.
- **Docker Process Sizing:** API pods run `gunicorn app:app -k uvicorn.workers.UvicornWorker` (`WEB_CONCURRENCY` ~ `2 * CPU + 1` or bounded by DB connection pool), separate from Celery worker containers (`celery -A proj worker`).
