from __future__ import annotations

import re

_BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE)
_API_KEY_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{8,}|AIza[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{10,}|jina_[A-Za-z0-9_-]{10,})\b"
)
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_CPF_RE = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

_GUARDRAIL_RULES: list[tuple[str, re.Pattern[str]]] = [
    (
        "prompt_injection",
        re.compile(
            r"\b(?:ignore|disregard)\s+(?:all\s+)?(?:previous|prior|system|above)\s+instructions\b"
            r"|\bsystem\s+override\b"
            r"|\bbypass\s+(?:all\s+)?(?:guardrails|policy|rules)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "system_prompt_exfil",
        re.compile(
            r"\b(?:reveal|print|show|output)\s+(?:your\s+|the\s+)?system\s+(?:prompt|instructions)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "solution_spoiler_request",
        re.compile(
            r"\b(?:give|show|dump|print|write|output)\s+(?:me\s+)?(?:the\s+)?"
            r"(?:full|complete|entire|exact)\s+(?:reference\s+)?(?:solution|answer|code)\b"
            r"|\bdump\s+solution\b",
            re.IGNORECASE,
        ),
    ),
]

_CITATION_RE = re.compile(r"\[(\d{2}-\d{2})\]")


def scrub_pii_and_secrets(text: str) -> str:
    """Redact credentials, API keys, emails, and government IDs before logging or LLM calls."""
    if not text:
        return ""
    cleaned = _BEARER_RE.sub("Bearer [TOKEN_REDACTED]", text)
    cleaned = _API_KEY_RE.sub("[API_KEY_REDACTED]", cleaned)
    cleaned = _EMAIL_RE.sub("[EMAIL_REDACTED]", cleaned)
    cleaned = _CPF_RE.sub("[GOV_ID_REDACTED]", cleaned)
    cleaned = _SSN_RE.sub("[GOV_ID_REDACTED]", cleaned)
    return cleaned


def detect_guardrail_violation(question: str) -> str | None:
    """Detect prompt-injection, system-prompt exfiltration, or full-solution spoiler requests."""
    if not question:
        return None
    for rule_name, pattern in _GUARDRAIL_RULES:
        if pattern.search(question):
            return rule_name
    return None


def verify_citations(text: str, valid_lesson_ids: set[str]) -> list[str]:
    """Extract deduplicated [XX-YY] lesson citations that exist in the known corpus."""
    seen: list[str] = []
    for match in _CITATION_RE.findall(text):
        if match in valid_lesson_ids and match not in seen:
            seen.append(match)
    return seen
