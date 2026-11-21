from __future__ import annotations

import re
from dataclasses import dataclass

from chunker import DocChunk

_CITATION_RE = re.compile(r"\[([a-zA-Z0-9_.:-]+)\]")
_WORD_RE = re.compile(r"[a-z0-9_]{4,}")
_STOPWORDS = {"that", "this", "with", "from", "when", "where", "which", "should", "have", "into"}


@dataclass(frozen=True)
class ClaimCheckResult:
    grounded: bool
    cited_ids: list[str]
    invalid_citations: list[str]
    reason: str | None = None


def verify_grounded_answer(answer: str, retrieved: list[DocChunk]) -> ClaimCheckResult:
    """Verify answer cites only retrieved chunk IDs and has lexical support in those chunks."""
    by_id = {chunk.chunk_id: chunk for chunk in retrieved}
    raw_cites = _CITATION_RE.findall(answer)
    valid_cites = [cid for cid in raw_cites if cid in by_id]
    invalid_cites = [cid for cid in raw_cites if cid not in by_id]

    if invalid_cites:
        return ClaimCheckResult(
            grounded=False,
            cited_ids=valid_cites,
            invalid_citations=invalid_cites,
            reason=f"Unknown citation(s): {', '.join(invalid_cites)}",
        )
    if not valid_cites:
        return ClaimCheckResult(
            grounded=False,
            cited_ids=[],
            invalid_citations=[],
            reason="Answer contains no verified citations",
        )

    prose_only = _CITATION_RE.sub(" ", answer).lower()
    ans_terms = {w for w in _WORD_RE.findall(prose_only) if w not in _STOPWORDS}
    cited_text = " ".join(by_id[cid].text.lower() for cid in valid_cites)
    cited_terms = set(_WORD_RE.findall(cited_text))
    overlap = ans_terms & cited_terms
    if not overlap:
        return ClaimCheckResult(
            grounded=False,
            cited_ids=valid_cites,
            invalid_citations=[],
            reason="Cited chunks do not support the claims in the answer",
        )

    return ClaimCheckResult(
        grounded=True,
        cited_ids=list(dict.fromkeys(valid_cites)),
        invalid_citations=[],
        reason=None,
    )
