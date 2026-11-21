from __future__ import annotations

import time

from pyquest.domain.models import LessonSpec, OracleCitation, OracleResponse
from pyquest.rag.interfaces import RagPipeline


class StubOracleService(RagPipeline):
    """Deterministic DIY Capstone placeholder until the learner builds their RAG engine in src/pyquest/rag/."""

    def ask(
        self,
        lesson: LessonSpec,
        question: str,
        files: dict[str, str],
        last_diagnostics: str = "",
    ) -> OracleResponse:
        started = time.perf_counter()
        cleaned_q = question.strip()
        file_names = ", ".join(sorted(files.keys())) or lesson.entry_file
        source_path = f"curriculum/{lesson.module_id}/{lesson.id}/concept.md"
        diag_note = (
            f"\n\nLatest diagnostic signal:\n> `{last_diagnostics.splitlines()[0]}`"
            if last_diagnostics.strip()
            else ""
        )

        first_hint = lesson.hints[0] if lesson.hints else lesson.objective
        answer = (
            f"**Oracle (DIY RAG Capstone Stub)** — active stage `[{lesson.id}] {lesson.title}`\n\n"
            "The live Socratic RAG Oracle is intentionally left as **your hands-on capstone** inside "
            "`src/pyquest/rag/` (see `src/pyquest/rag/CAPSTONE_README.md`). Implement `VectorStore`, "
            "`EmbeddingClient`, `LlmClient`, and `RagPipeline` to turn on live grounded retrieval + LLM answers!\n\n"
            f"- **Question received:** `{cleaned_q or '(empty)'}`\n"
            f"- **Active files:** `{file_names}`\n"
            f"- **Stage objective:** {lesson.objective}\n"
            f"- **Starter nudge:** {first_hint}"
            f"{diag_note}"
        )
        elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
        return OracleResponse(
            answer=answer,
            provider="stub",
            mode="stub",
            citations=[
                OracleCitation(
                    lesson_id=lesson.id,
                    title=lesson.title,
                    snippet=lesson.objective,
                    score=1.0,
                )
            ],
            cited_sources=[source_path],
            guardrail_triggered=False,
            latency_ms=elapsed_ms,
        )
