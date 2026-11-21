from __future__ import annotations

import math
import re
from typing import Protocol

from chunker import DocChunk

_TOKEN_RE = re.compile(r"[a-z0-9_]+")


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return max(0.0, dot / (norm_a * norm_b))


def _lexical_score(query: str, text: str) -> float:
    q_tokens = set(_TOKEN_RE.findall(query.lower()))
    if not q_tokens:
        return 0.0
    t_tokens = set(_TOKEN_RE.findall(text.lower()))
    return len(q_tokens & t_tokens) / len(q_tokens)


class HybridRetriever:
    def __init__(self, chunks: list[DocChunk], embedder: Embedder) -> None:
        self._chunks = list(chunks)
        self._embedder = embedder
        self._vectors = embedder.embed([c.text for c in self._chunks]) if self._chunks else []

    def search(self, query: str, top_k: int = 3, alpha: float = 0.6) -> list[tuple[DocChunk, float]]:
        if not self._chunks or top_k <= 0:
            return []
        q_vec = self._embedder.embed([query])[0]
        scored: list[tuple[DocChunk, float]] = []
        for chunk, vec in zip(self._chunks, self._vectors, strict=True):
            cos = cosine_similarity(q_vec, vec)
            lex = _lexical_score(query, chunk.text)
            combined = alpha * cos + (1.0 - alpha) * lex
            scored.append((chunk, round(combined, 6)))
        scored.sort(key=lambda pair: (-pair[1], pair[0].chunk_id))
        return scored[:top_k]
