import re


def keyword_overlap(query: str, doc: str) -> float:
    """Return fraction of unique query words present in doc (0.0..1.0)."""
    q_words = set(re.findall(r"[a-z0-9]+", query.lower()))
    d_words = set(re.findall(r"[a-z0-9]+", doc.lower()))
    if not q_words:
        return 0.0
    return len(q_words & d_words) / len(q_words)


def dot_product(a: list[float], b: list[float]) -> float:
    """Return vector dot product sum(x * y)."""
    return sum(x * y for x, y in zip(a, b, strict=True))
