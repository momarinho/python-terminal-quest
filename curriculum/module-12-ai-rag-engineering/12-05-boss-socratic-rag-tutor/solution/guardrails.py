from __future__ import annotations

import re

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
_API_KEY_RE = re.compile(r"\b(?:sk-|AIza|ghp_)[A-Za-z0-9_-]{8,}\b")

_BLOCK_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("prompt_injection", re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior)\s+instructions\b", re.I)),
    ("system_prompt_exfil", re.compile(r"\breveal\s+(?:the\s+|your\s+)?system\s+prompt\b", re.I)),
    ("solution_leak", re.compile(r"\b(?:give|show|dump|write)\s+(?:me\s+)?(?:the\s+)?(?:full|complete|entire)\s+(?:solution|answer|code)\b", re.I)),
    ("dump_solution", re.compile(r"\bdump\s+solution\b", re.I)),
]


def scrub_secrets(text: str) -> str:
    cleaned = _BEARER_RE.sub("Bearer [TOKEN_REDACTED]", text)
    cleaned = _API_KEY_RE.sub("[API_KEY_REDACTED]", cleaned)
    cleaned = _EMAIL_RE.sub("[EMAIL_REDACTED]", cleaned)
    return cleaned


def check_guardrail(question: str) -> str | None:
    for reason, pattern in _BLOCK_PATTERNS:
        if pattern.search(question):
            return reason
    return None
