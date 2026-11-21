# Idempotency Keys & SHA-256 Request Fingerprinting

Clients retry HTTP `POST` commands whenever a network timeout drops the response. Without an **Idempotency-Key**, a retry charges a card or creates a shipment twice.

## Two Failure Modes on Retries

1. **Duplicate Execution:** The server processes key `req-91` twice because it forgot the first response.
2. **Silent Key Reuse (Buggy Client):** A client reuses `Idempotency-Key: req-91` for a *different* payload (`qty=5` instead of `qty=1`). Replaying the cached `qty=1` receipt hides a client bug—you must fail loudly with a conflict error (`409` / `422`).

## Canonical Request Fingerprinting

Always hash a **canonical** JSON serialization (`sort_keys=True, separators=(",", ":")`) so key ordering never produces false mismatches:

```python
import hashlib
import json

def canonical_fingerprint(sku: str, quantity: int) -> str:
    payload = json.dumps({"sku": sku, "quantity": quantity}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

## Handler Lifecycle

1. Reject missing or whitespace-only `idempotency_key` upfront.
2. Compute `payload_hash`.
3. Look up `idempotency_key` in your store:
   - **Hit with matching `payload_hash`:** return the stored result marked `replayed=True` without invoking the side-effect executor.
   - **Hit with mismatched `payload_hash`:** raise an explicit conflict exception.
   - **Miss:** run the executor once, persist `(key, payload_hash, result)`, and return `replayed=False`.
