from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DocChunk:
    chunk_id: str
    doc_id: str
    text: str


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def chunk_document(
    doc_id: str,
    text: str,
    max_chars: int = 200,
    overlap_sentences: int = 1,
) -> list[DocChunk]:
    """Split text into sentence-aligned overlapping chunks."""
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return []
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(cleaned) if s.strip()]
    chunks: list[DocChunk] = []
    idx = 0

    while idx < len(sentences):
        current: list[str] = []
        cursor = idx
        while cursor < len(sentences):
            candidate = " ".join([*current, sentences[cursor]])
            if current and len(candidate) > max_chars:
                break
            current.append(sentences[cursor])
            cursor += 1

        chunk_id = f"{doc_id}:{len(chunks)}"
        chunks.append(DocChunk(chunk_id=chunk_id, doc_id=doc_id, text=" ".join(current)))
        if cursor >= len(sentences):
            break
        step = max(1, len(current) - max(0, overlap_sentences))
        idx += step

    return chunks
