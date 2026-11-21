from __future__ import annotations

import re

_INJECTION_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("ignore_instructions", re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior)\s+instructions\b", re.I)),
    ("reveal_system_prompt", re.compile(r"\breveal\s+(?:the\s+|your\s+)?system\s+prompt\b", re.I)),
    ("disregard_guardrails", re.compile(r"\bdisregard\s+(?:all\s+)?(?:rules|guardrails|policy)\b", re.I)),
    ("system_override", re.compile(r"\bsystem\s+override\s*:", re.I)),
    ("bypass_policy", re.compile(r"\bbypass\s+(?:security|policy|guardrails)\b", re.I)),
]


def detect_prompt_injection(text: str) -> str | None:
    """Return triggered guardrail rule name if prompt injection is detected, else None."""
    # TODO: Scan text against _INJECTION_RULES and return the first matched rule name
    raise NotImplementedError("TODO: detect_prompt_injection")
