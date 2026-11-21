from __future__ import annotations

from typing import Protocol

from chunker import DocChunk


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


def cosine_similarity(a: list[float], b: list[float]) -> float:
    # TODO: Compute safe cosine similarity returning 0.0 on zero-norm vectors
    raise NotImplementedError("TODO: cosine_similarity")


class HybridRetriever:
    def __init__(self, chunks: list[DocChunk], embedder: Embedder) -> None:
        self._chunks = list(chunks)
        self._embedder = embedder
        self._vectors = embedder.embed([c.text for c in self._chunks]) if self._chunks else []

    def search(self, query: str, top_k: int = 3, alpha: float = 0.6) -> list[tuple[DocChunk, float]]:
        # TODO: Combine alpha * cosine + (1 - alpha) * lexical keyword score, return top_k descending
        raise NotImplementedError("TODO: HybridRetriever.search")
