from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocChunk:
    chunk_id: str
    doc_id: str
    text: str


def chunk_document(
    doc_id: str,
    text: str,
    max_chars: int = 200,
    overlap_sentences: int = 1,
) -> list[DocChunk]:
    """Split text into sentence-aligned overlapping chunks."""
    # TODO: Split into sentences, pack <= max_chars with overlap_sentences carry-over
    raise NotImplementedError("TODO: chunk_document")
