from __future__ import annotations

import re
from typing import Literal, Protocol

from pydantic import BaseModel, Field


class StructuredOutputExhaustedError(RuntimeError):
    """Raised when the LLM fails to produce valid structured output within max_retries."""


class IncidentTriage(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    root_cause: str = Field(min_length=5)
    retryable: bool
    action_items: list[str] = Field(min_length=1)


class LlmClient(Protocol):
    def complete(self, prompt: str) -> str: ...


_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


def extract_json_block(raw_text: str) -> str:
    """Strip markdown code fences and isolate the JSON object substring."""
    # TODO: Handle fenced ```json ... ``` blocks as well as raw prose + {...}
    raise NotImplementedError("TODO: extract_json_block")


def generate_structured_triage(
    client: LlmClient,
    event_summary: str,
    max_retries: int = 2,
) -> tuple[IncidentTriage, int]:
    """Call client and retry with Pydantic ValidationError feedback up to max_retries."""
    # TODO: Loop up to 1 + max_retries calls; return (model, attempts_used) or raise StructuredOutputExhaustedError
    raise NotImplementedError("TODO: generate_structured_triage")
