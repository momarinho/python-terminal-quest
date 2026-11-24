import math  # noqa: F401
import re  # noqa: F401


def estimate_tokens(text: str) -> int:
    """Estimate token count with ceil(len(text) / 4), returning 0 when empty."""
    return -1


def redact_api_key(text: str) -> str:
    """Replace 'sk-<6+ alnum chars>' tokens with '[REDACTED]'."""
    return text
