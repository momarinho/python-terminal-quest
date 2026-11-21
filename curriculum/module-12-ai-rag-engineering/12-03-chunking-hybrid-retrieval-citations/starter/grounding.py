from __future__ import annotations

from dataclasses import dataclass

from chunker import DocChunk


@dataclass(frozen=True)
class ClaimCheckResult:
    grounded: bool
    cited_ids: list[str]
    invalid_citations: list[str]
    reason: str | None = None


def verify_grounded_answer(answer: str, retrieved: list[DocChunk]) -> ClaimCheckResult:
    """Verify answer cites only retrieved chunk IDs and has lexical support in those chunks."""
    # TODO: Extract [chunk_id] markers, validate against retrieved chunks, and check lexical overlap
    raise NotImplementedError("TODO: verify_grounded_answer")
