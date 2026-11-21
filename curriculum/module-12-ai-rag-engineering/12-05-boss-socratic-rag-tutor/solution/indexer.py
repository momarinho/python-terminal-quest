from __future__ import annotations

import math
import re
from dataclasses import dataclass

_TOKEN_RE = re.compile(r"[a-z0-9_]{2,}")


class SolutionLeakError(ValueError):
    """Raised if caller attempts to index a solution file into the RAG corpus."""


@dataclass(frozen=True)
class IndexedChunk:
    lesson_id: str
    title: str
    text: str


class CurriculumIndex:
    def __init__(self) -> None:
        self._chunks: list[IndexedChunk] = []

    def add_document(
        self,
        lesson_id: str,
        title: str,
        concept_md: str,
        *,
        source_path: str = "",
        is_solution: bool = False,
    ) -> int:
        normalized_path = source_path.replace("\\", "/").lower()
        if is_solution or "/solution/" in normalized_path or normalized_path.startswith("solution/"):
            raise SolutionLeakError(
                f"Refusing to index reference solution content for '{lesson_id}'"
            )

        paragraphs = [p.strip() for p in concept_md.split("\n\n") if p.strip()]
        added = 0
        for para in paragraphs:
            cleaned = " ".join(para.split())
            if cleaned:
                self._chunks.append(IndexedChunk(lesson_id=lesson_id, title=title, text=cleaned))
                added += 1
        return added

    def search(
        self,
        query: str,
        *,
        active_lesson_id: str | None = None,
        top_k: int = 3,
    ) -> list[tuple[IndexedChunk, float]]:
        if not self._chunks or top_k <= 0:
            return []
        q_tokens = _TOKEN_RE.findall(query.lower())
        if not q_tokens:
            return []
        q_set = set(q_tokens)

        scored: list[tuple[IndexedChunk, float]] = []
        for chunk in self._chunks:
            c_tokens = _TOKEN_RE.findall(f"{chunk.title} {chunk.text}".lower())
            c_set = set(c_tokens)
            overlap = q_set & c_set
            if not overlap and chunk.lesson_id != active_lesson_id:
                continue
            tf_score = sum(c_tokens.count(tok) for tok in overlap) / max(1, math.sqrt(len(c_tokens)))
            coverage = len(overlap) / len(q_set)
            lesson_boost = 0.35 if (active_lesson_id and chunk.lesson_id == active_lesson_id) else 0.0
            score = round(coverage * 0.7 + tf_score * 0.3 + lesson_boost, 6)
            if score > 0.0:
                scored.append((chunk, score))

        scored.sort(key=lambda pair: (-pair[1], pair[0].lesson_id))
        return scored[:top_k]
