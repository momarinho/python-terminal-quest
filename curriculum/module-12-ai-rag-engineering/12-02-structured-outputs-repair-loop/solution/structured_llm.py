from __future__ import annotations

import re
from typing import Literal, Protocol

from pydantic import BaseModel, Field, ValidationError


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
    fenced = _FENCE_RE.search(raw_text)
    if fenced:
        return fenced.group(1).strip()
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM response")
    return raw_text[start : end + 1].strip()


def generate_structured_triage(
    client: LlmClient,
    event_summary: str,
    max_retries: int = 2,
) -> tuple[IncidentTriage, int]:
    """Call client and retry with Pydantic ValidationError feedback up to max_retries."""
    base_prompt = f"Classify incident and respond with JSON matching IncidentTriage:\n{event_summary}"
    prompt = base_prompt
    last_error = ""

    for attempt in range(1, max_retries + 2):
        raw = client.complete(prompt)
        try:
            json_text = extract_json_block(raw)
            model = IncidentTriage.model_validate_json(json_text)
            return model, attempt
        except (ValidationError, ValueError) as exc:
            last_error = str(exc)
            prompt = (
                f"{base_prompt}\n\n"
                f"Previous response failed validation with error:\n{last_error}\n"
                "Return ONLY a valid JSON object matching the schema."
            )

    raise StructuredOutputExhaustedError(
        f"Failed after {max_retries + 1} attempts. Last error: {last_error}"
    )
