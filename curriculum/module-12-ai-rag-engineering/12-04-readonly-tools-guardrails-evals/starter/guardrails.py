from __future__ import annotations

import re

# TODO: compile (rule_name, pattern) tuples for:
# ignore_instructions, reveal_system_prompt, disregard_guardrails, system_override, bypass_policy
_INJECTION_RULES: list[tuple[str, re.Pattern[str]]] = []


def detect_prompt_injection(text: str) -> str | None:
    """Return triggered guardrail rule name if prompt injection is detected, else None."""
    _ = _INJECTION_RULES
    raise NotImplementedError("TODO: detect_prompt_injection")
