from __future__ import annotations

from pyquest.domain.models import LessonSpec, OracleResponse
from pyquest.rag.interfaces import RagPipeline


class StubOracleService(RagPipeline):
    """Deterministic local Oracle stub ready to swap for live Gemini/Ollama RAG in Wave 3."""

    def ask(
        self,
        lesson: LessonSpec,
        question: str,
        files: dict[str, str],
        last_diagnostics: str = "",
    ) -> OracleResponse:
        cleaned_q = question.strip()
        file_names = ", ".join(sorted(files.keys())) or lesson.entry_file
        diag_note = (
            f"\n\nLatest diagnostic signal:\n> `{last_diagnostics.splitlines()[0]}`"
            if last_diagnostics.strip()
            else ""
        )

        # Offer targeted guidance based on keywords while staying strictly spoiler-free
        q_lower = cleaned_q.lower()
        if "decimal" in q_lower or "float" in q_lower:
            guidance = (
                "Prefer `Decimal` constructed from `str` values (`Decimal('0.10')`) rather than "
                "binary `float` literals, and avoid mixing `float` and `Decimal` in arithmetic."
            )
        elif "syntax" in q_lower or "indent" in q_lower:
            guidance = (
                "Check the highlighted red squiggle line in Monaco: Python `SyntaxError` / "
                "`IndentationError` diagnostics usually point to an unclosed delimiter or mismatched block indent."
            )
        elif "mutable" in q_lower or "default" in q_lower:
            guidance = (
                "Never use `[]` or `{}` as a default parameter value—default to `None` and "
                "initialize a fresh collection inside the function body."
            )
        else:
            first_hint = lesson.hints[0] if lesson.hints else lesson.objective
            guidance = (
                f"Focus on the stage objective: **{lesson.objective}**\n\n"
                f"Starting nudge for `{file_names}`: {first_hint}"
            )

        answer = (
            f"**Oracle (Local Stub)** analyzing stage `{lesson.id} — {lesson.title}`:\n\n"
            f"{guidance}{diag_note}\n\n"
            f"_Tip: Run `Ctrl+Enter` to inspect pytest's root-cause diff, or unlock progressive hints in the Hints tab._"
        )
        return OracleResponse(
            answer=answer,
            provider="stub-local",
            cited_sources=[f"curriculum/{lesson.module_id}/{lesson.id}/concept.md"],
        )
