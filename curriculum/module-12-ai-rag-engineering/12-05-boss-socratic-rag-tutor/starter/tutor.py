from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

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
        # TODO: Scrub secrets -> run check_guardrail -> retrieve top chunks -> return grounded SocraticTutorResponse
        raise NotImplementedError("TODO: SocraticRagTutor.ask")
