import hashlib  # noqa: F401
import hmac  # noqa: F401


def sha256_hex(payload: str) -> str:
    """Return lowercase SHA-256 hex digest of UTF-8 payload."""
    # Reveal: return hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return ""


def sign_hmac(secret: str, message: str) -> str:
    """Compute hex HMAC-SHA256 signature for message using secret."""
    # Reveal: return hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    return ""


def verify_hmac(secret: str, message: str, signature: str) -> bool:
    """Verify HMAC signature in constant time."""
    # Reveal: return hmac.compare_digest(sign_hmac(secret, message), signature)
    return False
