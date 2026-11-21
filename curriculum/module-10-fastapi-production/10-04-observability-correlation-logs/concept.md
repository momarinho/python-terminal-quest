## Concept: `contextvars` Correlation IDs, Structured Logs & Metrics

Under concurrent `asyncio` requests, thread-local variables bleed across coroutines. Python's **`contextvars.ContextVar`** gives each async task its own isolated request context!

### Safe `ContextVar` Binding (`set` / `reset` in `finally`)
```python
from contextvars import ContextVar

TRACE_ID_CTX: ContextVar[str | None] = ContextVar("trace_id", default=None)

token = TRACE_ID_CTX.set(incoming_id)
try:
    response = await call_next(request)
finally:
    TRACE_ID_CTX.reset(token)
```

* Always reset the `ContextVar` using the returned `token` inside `finally:` so reused worker tasks never leak an earlier request's ID!
* Emit machine-parseable JSON log dictionaries (`request_id`, `method`, `path`, `status_code`, `duration_ms`) and echo `X-Request-ID` in response headers for client support debugging.

### Challenge
Implement `REQUEST_ID_CTX`, `MetricsRegistry`, and `ObservabilityMiddleware` in `observability.py`, and wire `/work` (reading `REQUEST_ID_CTX.get()`) + `/metrics` in `app.py`.
