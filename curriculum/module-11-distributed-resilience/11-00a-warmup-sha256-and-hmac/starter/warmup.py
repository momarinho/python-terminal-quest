import hashlib  # noqa: F401
import hmac  # noqa: F401


def sha256_hex(payload: str) -> str:
    """Return lowercase SHA-256 hex digest."""
    return ""


def sign_hmac(secret: str, message: str) -> str:
    """Return hex HMAC-SHA256 signature."""
    return ""


def verify_hmac(secret: str, message: str, signature: str) -> bool:
    """Verify HMAC signature in constant time."""
    return False
