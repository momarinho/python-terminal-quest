import math
import re


def estimate_tokens(text: str) -> int:
    """Estimate token count with ceil(len(text) / 4), returning 0 when empty."""
    return math.ceil(len(text) / 4) if text else 0


def redact_api_key(text: str) -> str:
    """Replace 'sk-<6+ alnum chars>' tokens with '[REDACTED]'."""
    return re.sub(r"sk-[A-Za-z0-9]{6,}", "[REDACTED]", text)
