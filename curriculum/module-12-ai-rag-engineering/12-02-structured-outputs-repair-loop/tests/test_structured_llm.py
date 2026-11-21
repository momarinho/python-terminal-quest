import pytest
from structured_llm import (
    StructuredOutputExhaustedError,
    extract_json_block,
    generate_structured_triage,
)


class ScriptedLlmClient:
    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        idx = min(len(self.prompts) - 1, len(self._responses) - 1)
        return self._responses[idx]


def test_extracts_fenced_json_and_repairs_validation_error() -> None:
    bad_first = '```json\n{"severity": "urgent", "root_cause": "db", "retryable": true, "action_items": []}\n```'
    good_second = (
        'Sure! Here is the JSON:\n```json\n'
        '{"severity": "high", "root_cause": "PostgreSQL connection pool saturated", '
        '"retryable": true, "action_items": ["Increase max_connections"]}\n```'
    )
    client = ScriptedLlmClient([bad_first, good_second])

    triage, attempts = generate_structured_triage(client, "Checkout 503 storm", max_retries=2)
    assert attempts == 2
    assert triage.severity == "high"
    assert triage.retryable is True
    assert len(client.prompts) == 2
    assert "severity" in client.prompts[1] or "action_items" in client.prompts[1]


def test_exhausted_retries_raises_explicit_error() -> None:
    client = ScriptedLlmClient(["not json at all"] * 4)
    with pytest.raises(StructuredOutputExhaustedError):
        generate_structured_triage(client, "Timeout event", max_retries=2)
    assert len(client.prompts) == 3
    assert extract_json_block('prefix {"a": 1} suffix') == '{"a": 1}'
