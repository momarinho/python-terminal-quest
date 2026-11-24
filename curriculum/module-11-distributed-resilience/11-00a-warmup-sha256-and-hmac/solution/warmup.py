import hashlib
import hmac


def sha256_hex(payload: str) -> str:
    """Return lowercase SHA-256 hex digest."""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sign_hmac(secret: str, message: str) -> str:
    """Return hex HMAC-SHA256 signature."""
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_hmac(secret: str, message: str, signature: str) -> bool:
    """Verify HMAC signature in constant time."""
    return hmac.compare_digest(sign_hmac(secret, message), signature)
