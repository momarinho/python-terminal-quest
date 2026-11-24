## Beginner Warm-Up 1: SHA-256 & HMAC Verification

Distributed systems fingerprint payloads with SHA-256 and authenticate webhooks with `hmac.compare_digest`:

```python
import hashlib
import hmac

def sha256_hex(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def verify_hmac(secret: str, message: str, signature: str) -> bool:
    expected = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Challenge
Implement `sha256_hex`, `sign_hmac`, and `verify_hmac` in `warmup.py`.
