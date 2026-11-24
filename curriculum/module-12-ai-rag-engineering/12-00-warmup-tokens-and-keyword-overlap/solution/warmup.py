import math
import re


def estimate_tokens(text: str) -> int:
    """Estimate token count using ceil(len(text) / 4), returning 0 when empty."""
    return math.ceil(len(text) / 4) if text else 0


def redact_api_key(text: str) -> str:
    """Replace 'sk-<6+ alnum chars>' tokens with '[REDACTED]'."""
    return re.sub(r"sk-[A-Za-z0-9]{6,}", "[REDACTED]", text)


def keyword_overlap_score(query: str, doc: str) -> float:
    """Return fraction of unique lowercase query words found in doc (0.0..1.0)."""
    q_words = set(re.findall(r"[a-z0-9]+", query.lower()))
    d_words = set(re.findall(r"[a-z0-9]+", doc.lower()))
    if not q_words:
        return 0.0
    return len(q_words & d_words) / len(q_words)
