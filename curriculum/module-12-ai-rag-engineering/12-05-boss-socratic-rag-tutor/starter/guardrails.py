from __future__ import annotations


def scrub_secrets(text: str) -> str:
    # TODO: Redact emails, Bearer tokens, and sk-/AIza/ghp_ API keys
    raise NotImplementedError("TODO: scrub_secrets")


def check_guardrail(question: str) -> str | None:
    # TODO: Return block reason if question attempts prompt injection or full-solution extraction, else None
    raise NotImplementedError("TODO: check_guardrail")
