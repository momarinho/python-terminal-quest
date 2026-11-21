from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from guardrails import check_guardrail, scrub_secrets
from indexer import CurriculumIndex


class TutorLlmClient(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str: ...


@dataclass(frozen=True)
class SocraticTutorResponse:
    answer: str
    citations: list[str]
    blocked: bool
    scrubbed_question: str


class SocraticRagTutor:
    def __init__(
        self,
        index: CurriculumIndex,
        llm_client: TutorLlmClient | None = None,
    ) -> None:
        self._index = index
        self._llm = llm_client

    def ask(self, lesson_id: str, question: str) -> SocraticTutorResponse:
        scrubbed = scrub_secrets(question.strip())
        violation = check_guardrail(scrubbed)
        if violation is not None:
            return SocraticTutorResponse(
                answer=(
                    f"Socratic Guardrail triggered ({violation}): I cannot bypass instructions "
                    "or reveal full reference solutions. Share what assertion failed and what hypothesis you're testing!"
                ),
                citations=[],
                blocked=True,
                scrubbed_question=scrubbed,
            )

        hits = self._index.search(scrubbed, active_lesson_id=lesson_id, top_k=3)
        citations = list(dict.fromkeys(chunk.lesson_id for chunk, _ in hits))
        context_lines = [f"[{chunk.lesson_id}] ({chunk.title}): {chunk.text}" for chunk, _ in hits]

        if self._llm is not None:
            sys_prompt = (
                "You are a Socratic Python coach. Guide using retrieved concept chunks and cite [lesson-id]. "
                "Never provide full copy-paste solutions."
            )
            user_prompt = (
                f"Active Lesson: {lesson_id}\nQuestion: {scrubbed}\n\n"
                f"Context:\n" + "\n".join(context_lines)
            )
            try:
                llm_answer = self._llm.generate(sys_prompt, user_prompt)
                return SocraticTutorResponse(
                    answer=llm_answer,
                    citations=citations,
                    blocked=False,
                    scrubbed_question=scrubbed,
                )
            except Exception:
                pass

        if hits:
            top_chunk, _ = hits[0]
            cited_tags = " ".join(f"[{cid}]" for cid in citations)
            answer = (
                f"Grounded hint from {cited_tags}: focus on `{top_chunk.title}` — "
                f"{top_chunk.text[:220]}. What invariant in your current implementation violates that rule?"
            )
        else:
            answer = (
                f"No direct concept excerpt matched `{scrubbed}`. Re-read lesson `{lesson_id}` "
                "and inspect the failing pytest diff to pinpoint the smallest broken invariant."
            )

        return SocraticTutorResponse(
            answer=answer,
            citations=citations,
            blocked=False,
            scrubbed_question=scrubbed,
        )
