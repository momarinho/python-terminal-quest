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
    # TODO: Apply the compiled regex patterns cleanly
    raise NotImplementedError("TODO: implement scrub_pii")


def trim_conversation_history(
    system_prompt: str,
    history: list[ChatMessage],
    current_query: str,
    max_tokens: int,
) -> list[ChatMessage]:
    """Scrub PII and trim oldest history turns to stay within max_tokens."""
    # TODO:
    # 1. Always preserve system_prompt first and scrubbed current_query last
    # 2. Raise ValueError if system_prompt + scrubbed current_query exceed max_tokens
    # 3. Walk history newest -> oldest adding scrubbed turns that fit in remaining budget
    raise NotImplementedError("TODO: implement trim_conversation_history")
