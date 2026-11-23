from __future__ import annotations

import re

from pyquest.domain.models import LessonSpec
from pyquest.rag.interfaces import DocumentChunk

_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.MULTILINE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


class SolutionLeakError(ValueError):
    """Raised when a caller attempts to index reference solution or test files."""


def validate_safe_corpus_path(source_path: str, *, is_solution: bool = False) -> None:
    """Enforce zero-leak corpus invariant by blocking solution/ and tests/ paths."""
    normalized = source_path.replace("\\", "/").strip().lower()
    segments = [seg for seg in normalized.split("/") if seg]
    if is_solution or any(seg in {"solution", "solutions", "tests"} for seg in segments):
        raise SolutionLeakError(
            f"Refusing to index restricted solution or test path: '{source_path}'"
        )


def _split_long_block(text: str, max_chars: int) -> list[str]:
    """Split a long block along paragraph and sentence boundaries with 1-sentence overlap."""
    cleaned = text.strip()
    if not cleaned:
        return []
    if len(cleaned) <= max_chars:
        return [cleaned]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    sentences: list[str] = []
    for para in paragraphs:
        if len(para) <= max_chars:
            sentences.append(para)
        else:
            parts = [s.strip() for s in _SENTENCE_SPLIT_RE.split(para) if s.strip()]
            sentences.extend(parts or [para])

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for sentence in sentences:
        sep_len = 1 if current else 0
        if current and current_len + sep_len + len(sentence) > max_chars:
            chunks.append(" ".join(current))
            overlap = current[-1:] if len(current[-1]) < max_chars // 2 else []
            current = [*overlap, sentence]
            current_len = sum(len(item) for item in current) + max(0, len(current) - 1)
        else:
            current.append(sentence)
            current_len += sep_len + len(sentence)

    if current:
        chunks.append(" ".join(current))
    return chunks


def _extract_markdown_sections(markdown: str) -> list[tuple[str, str]]:
    """Split concept.md into (section_title, body_text) pairs."""
    matches = list(_HEADING_RE.finditer(markdown))
    if not matches:
        body = markdown.strip()
        return [("Overview", body)] if body else []

    sections: list[tuple[str, str]] = []
    preamble = markdown[: matches[0].start()].strip()
    if preamble:
        sections.append(("Overview", preamble))

    for idx, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        if body:
            sections.append((title, f"{title}\n{body}"))
    return sections


def chunk_lesson_markdown(
    lesson: LessonSpec,
    *,
    source_path: str | None = None,
    is_solution: bool = False,
    max_chars: int = 700,
) -> list[DocumentChunk]:
    """Chunk a single LessonSpec safely from concept.md + lesson metadata."""
    effective_source = source_path or f"curriculum/{lesson.module_id}/{lesson.id}/concept.md"
    validate_safe_corpus_path(effective_source, is_solution=is_solution)

    base_meta = {
        "lesson_id": lesson.id,
        "title": lesson.title,
        "module_id": lesson.module_id,
        "tags": ",".join(lesson.tags),
    }

    chunks: list[DocumentChunk] = [
        DocumentChunk(
            chunk_id=f"{lesson.id}:meta",
            source=effective_source,
            content=(
                f"[{lesson.id}] {lesson.title} ({lesson.module_title}). "
                f"Objective: {lesson.objective}. "
                f"Tags: {', '.join(lesson.tags)}."
            ),
            metadata={**base_meta, "section": "Objective"},
        )
    ]

    seq = 0
    for section_title, section_body in _extract_markdown_sections(lesson.concept_markdown):
        for piece in _split_long_block(section_body, max_chars=max_chars):
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{lesson.id}:s{seq}",
                    source=effective_source,
                    content=piece,
                    metadata={**base_meta, "section": section_title},
                )
            )
            seq += 1

    return chunks


def index_curriculum_lessons(lessons: list[LessonSpec]) -> list[DocumentChunk]:
    """Build all safe DocumentChunks across the loaded curriculum lessons."""
    all_chunks: list[DocumentChunk] = []
    for lesson in lessons:
        all_chunks.extend(chunk_lesson_markdown(lesson))
    return all_chunks
