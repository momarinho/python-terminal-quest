from __future__ import annotations

from dataclasses import dataclass


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
        # TODO: Reject solution paths / is_solution=True with SolutionLeakError; chunk concept_md into IndexedChunk entries
        raise NotImplementedError("TODO: add_document")

    def search(
        self,
        query: str,
        *,
        active_lesson_id: str | None = None,
        top_k: int = 3,
    ) -> list[tuple[IndexedChunk, float]]:
        # TODO: Score chunks by keyword/TF similarity + active_lesson_id boost, return top_k descending
        raise NotImplementedError("TODO: search")
