from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str


_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_GOV_ID_RE = re.compile(r"\b(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{3}-\d{2}-\d{4})\b")
_BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
_API_KEY_RE = re.compile(r"\b(?:sk-|AIza|ghp_)[A-Za-z0-9_-]{8,}\b")


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return math.ceil(len(text) / 4)


def scrub_pii(text: str) -> str:
    """Redact emails, CPF/SSN IDs, bearer tokens, and common API keys."""
    cleaned = _BEARER_RE.sub("Bearer [TOKEN_REDACTED]", text)
    cleaned = _API_KEY_RE.sub("[API_KEY_REDACTED]", cleaned)
    cleaned = _EMAIL_RE.sub("[EMAIL_REDACTED]", cleaned)
    cleaned = _GOV_ID_RE.sub("[GOV_ID_REDACTED]", cleaned)
    return cleaned


def trim_conversation_history(
    system_prompt: str,
    history: list[ChatMessage],
    current_query: str,
    max_tokens: int,
) -> list[ChatMessage]:
    """Scrub PII and trim oldest history turns to stay within max_tokens."""
    clean_system = scrub_pii(system_prompt)
    clean_query = scrub_pii(current_query)
    base_cost = estimate_tokens(clean_system) + estimate_tokens(clean_query)
    if base_cost > max_tokens:
        raise ValueError(
            f"System prompt + current query ({base_cost} tokens) exceed budget ({max_tokens})"
        )

    remaining = max_tokens - base_cost
    kept_reversed: list[ChatMessage] = []
    for msg in reversed(history):
        clean_msg = ChatMessage(role=msg.role, content=scrub_pii(msg.content))
        cost = estimate_tokens(clean_msg.content)
        if cost <= remaining:
            kept_reversed.append(clean_msg)
            remaining -= cost

    kept = list(reversed(kept_reversed))
    return [
        ChatMessage(role="system", content=clean_system),
        *kept,
        ChatMessage(role="user", content=clean_query),
    ]
