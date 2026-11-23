from __future__ import annotations

import hashlib
import math
import re
from collections import Counter

from pyquest.rag.interfaces import (
    DocumentChunk,
    EmbeddingClient,
    ScoredChunk,
    VectorStore,
)

_TOKEN_RE = re.compile(r"[a-z0-9_]{2,}")


def tokenize_for_search(text: str) -> list[str]:
    """Extract normalized word and snake_case sub-tokens for lexical & dense matching."""
    tokens: list[str] = []
    for match in _TOKEN_RE.findall(text.lower()):
        tokens.append(match)
        if "_" in match:
            for part in match.split("_"):
                if len(part) >= 2 and part != match:
                    tokens.append(part)
    return tokens


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b, strict=False))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a <= 0.0 or norm_b <= 0.0:
        return 0.0
    return max(0.0, dot / (norm_a * norm_b))


class LocalHashedEmbeddingClient(EmbeddingClient):
    """Zero-dependency deterministic dense embedding model using Blake2b n-gram projections."""

    def __init__(self, dim: int = 256) -> None:
        if dim <= 0:
            raise ValueError("dim must be positive")
        self._dim = dim

    def _accumulate(self, vector: list[float], feature: str, weight: float) -> None:
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        bucket = int.from_bytes(digest[:4], "little") % self._dim
        sign = 1.0 if (digest[4] & 1) == 0 else -1.0
        vector[bucket] += sign * weight

    def _embed_one(self, text: str) -> list[float]:
        vec = [0.0] * self._dim
        tokens = tokenize_for_search(text)
        if not tokens:
            return vec

        counts = Counter(tokens)
        for token, freq in counts.items():
            tf_weight = 1.0 + math.log(freq)
            self._accumulate(vec, f"w:{token}", tf_weight * 1.4)
            if len(token) >= 3:
                for i in range(len(token) - 2):
                    self._accumulate(vec, f"c:{token[i : i + 3]}", 0.35)

        for idx in range(len(tokens) - 1):
            self._accumulate(vec, f"bg:{tokens[idx]}|{tokens[idx + 1]}", 0.7)

        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0.0:
            return [v / norm for v in vec]
        return vec

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]


class HybridRrfVectorStore(VectorStore):
    """Hybrid Okapi BM25 + dense vector store using Reciprocal Rank Fusion (RRF)."""

    def __init__(self, *, k1: float = 1.5, b: float = 0.75, k_rrf: int = 30) -> None:
        self._k1 = k1
        self._b = b
        self._k_rrf = k_rrf
        self._chunks: list[DocumentChunk] = []
        self._embeddings: list[list[float]] = []
        self._chunk_idx_by_id: dict[str, int] = {}
        self._doc_term_freqs: list[Counter[str]] = []
        self._doc_lengths: list[int] = []
        self._doc_freqs: Counter[str] = Counter()
        self._avgdl: float = 1.0

    def _rebuild_bm25_stats(self) -> None:
        self._doc_term_freqs = []
        self._doc_lengths = []
        self._doc_freqs = Counter()
        for chunk in self._chunks:
            tokens = tokenize_for_search(chunk.content)
            tf = Counter(tokens)
            self._doc_term_freqs.append(tf)
            self._doc_lengths.append(len(tokens))
            for term in tf:
                self._doc_freqs[term] += 1
        total_len = sum(self._doc_lengths)
        self._avgdl = (total_len / len(self._chunks)) if self._chunks else 1.0

    def upsert(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have identical lengths")
        for chunk, emb in zip(chunks, embeddings, strict=True):
            existing_idx = self._chunk_idx_by_id.get(chunk.chunk_id)
            if existing_idx is not None:
                self._chunks[existing_idx] = chunk
                self._embeddings[existing_idx] = emb
            else:
                self._chunk_idx_by_id[chunk.chunk_id] = len(self._chunks)
                self._chunks.append(chunk)
                self._embeddings.append(emb)
        self._rebuild_bm25_stats()

    def _matches_filter(
        self, chunk: DocumentChunk, filter_metadata: dict[str, str] | None
    ) -> bool:
        if not filter_metadata:
            return True
        return all(chunk.metadata.get(key) == val for key, val in filter_metadata.items())

    def _bm25_score(self, doc_idx: int, query_terms: list[str]) -> float:
        if not query_terms or not self._chunks:
            return 0.0
        n_docs = len(self._chunks)
        tf_map = self._doc_term_freqs[doc_idx]
        doc_len = self._doc_lengths[doc_idx]
        score = 0.0
        for term in query_terms:
            tf = tf_map.get(term, 0)
            if tf <= 0:
                continue
            df = self._doc_freqs.get(term, 0)
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
            denom = tf + self._k1 * (1.0 - self._b + self._b * (doc_len / max(self._avgdl, 1.0)))
            score += idf * ((tf * (self._k1 + 1.0)) / denom)
        return score

    def query(
        self,
        embedding: list[float],
        *,
        top_k: int = 5,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[ScoredChunk]:
        if top_k <= 0 or not self._chunks:
            return []
        scored: list[ScoredChunk] = []
        for idx, chunk in enumerate(self._chunks):
            if not self._matches_filter(chunk, filter_metadata):
                continue
            sim = _cosine_similarity(embedding, self._embeddings[idx])
            scored.append(ScoredChunk(chunk=chunk, score=round(min(1.0, sim), 4)))
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def hybrid_query(
        self,
        query_text: str,
        query_embedding: list[float],
        *,
        top_k: int = 4,
        active_lesson_id: str | None = None,
        filter_metadata: dict[str, str] | None = None,
        max_per_lesson: int = 2,
    ) -> list[ScoredChunk]:
        if top_k <= 0 or not self._chunks:
            return []

        query_terms = list(dict.fromkeys(tokenize_for_search(query_text)))
        candidates: list[tuple[int, float, float]] = []
        for idx, chunk in enumerate(self._chunks):
            if not self._matches_filter(chunk, filter_metadata):
                continue
            bm25 = self._bm25_score(idx, query_terms)
            cos = _cosine_similarity(query_embedding, self._embeddings[idx])
            candidates.append((idx, bm25, cos))

        if not candidates:
            return []

        max_bm25 = max((item[1] for item in candidates), default=0.0) or 1.0
        max_cos = max((item[2] for item in candidates), default=0.0) or 1.0

        bm25_ranked = sorted(candidates, key=lambda x: x[1], reverse=True)
        cos_ranked = sorted(candidates, key=lambda x: x[2], reverse=True)
        bm25_rank_map = {
            idx: rank for rank, (idx, score, _) in enumerate(bm25_ranked, start=1) if score > 0
        }
        cos_rank_map = {
            idx: rank for rank, (idx, _, score) in enumerate(cos_ranked, start=1) if score > 0
        }

        combined: list[tuple[DocumentChunk, float]] = []
        for idx, bm25, cos in candidates:
            chunk = self._chunks[idx]
            norm_bm25 = bm25 / max_bm25 if bm25 > 0 else 0.0
            norm_cos = cos / max_cos if cos > 0 else 0.0

            rrf = 0.0
            if idx in bm25_rank_map:
                rrf += 1.0 / (self._k_rrf + bm25_rank_map[idx])
            if idx in cos_rank_map:
                rrf += 1.0 / (self._k_rrf + cos_rank_map[idx])
            max_possible_rrf = 2.0 / (self._k_rrf + 1)
            norm_rrf = rrf / max_possible_rrf

            raw_score = 0.45 * norm_bm25 + 0.30 * norm_cos + 0.25 * norm_rrf
            if active_lesson_id and chunk.metadata.get("lesson_id") == active_lesson_id and (
                bm25 > 0.0 or cos > 0.08 or not query_terms
            ):
                raw_score += 0.18
            if raw_score > 0.0:
                combined.append((chunk, raw_score))

        combined.sort(key=lambda pair: pair[1], reverse=True)

        selected: list[ScoredChunk] = []
        per_lesson_counts: Counter[str] = Counter()
        for chunk, score in combined:
            lid = chunk.metadata.get("lesson_id", chunk.chunk_id)
            if per_lesson_counts[lid] >= max_per_lesson:
                continue
            per_lesson_counts[lid] += 1
            selected.append(ScoredChunk(chunk=chunk, score=round(min(1.0, score), 4)))
            if len(selected) >= top_k:
                break
        return selected
