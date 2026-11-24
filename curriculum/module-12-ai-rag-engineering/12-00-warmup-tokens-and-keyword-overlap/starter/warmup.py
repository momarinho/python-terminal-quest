import math  # noqa: F401
import re  # noqa: F401


def estimate_tokens(text: str) -> int:
    """Estimate token count using ceil(len(text) / 4), returning 0 when empty."""
    # Reveal: return math.ceil(len(text) / 4) if text else 0
    return -1


def redact_api_key(text: str) -> str:
    """Replace 'sk-<6+ alnum chars>' tokens with '[REDACTED]'."""
    # Reveal: return re.sub(r"sk-[A-Za-z0-9]{6,}", "[REDACTED]", text)
    return text


def keyword_overlap_score(query: str, doc: str) -> float:
    """Return fraction of unique lowercase query words found in doc (0.0..1.0)."""
    # Reveal: len(q_words & d_words) / len(q_words)
    return 0.0
