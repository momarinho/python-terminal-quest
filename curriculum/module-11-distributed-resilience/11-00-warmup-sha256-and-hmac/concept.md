## Concept: Warm-Up & Quick Syntax Reveal (Module 11)

Distributed systems rely on deterministic payload fingerprints (idempotency keys) and constant-time HMAC signature verification (webhooks). Practice both in 3 tiny helpers!

### Pattern Reveal #1 — SHA-256 Hex Digest
```python
import hashlib

def sha256_hex(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

### Pattern Reveal #2 — Signing with HMAC-SHA256
```python
import hmac

def sign_hmac(secret: str, message: str) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
```

### Pattern Reveal #3 — Constant-Time Comparison (`hmac.compare_digest`)
```python
def verify_hmac(secret: str, message: str, signature: str) -> bool:
    return hmac.compare_digest(sign_hmac(secret, message), signature)
```

### Challenge
Open `warmup.py` and complete `sha256_hex`, `sign_hmac`, and `verify_hmac`.
