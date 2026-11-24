from __future__ import annotations

import math
import re

from pyquest.domain.models import OracleTurn

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
_FENCED_BLOCK_RE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def approx_tokens(text: str) -> int:
    """Deterministic lightweight token estimator (~4 chars per token)."""
    return math.ceil(len(text) / 4) if text else 0


def trim_history_to_token_budget(
    history: list[OracleTurn],
    *,
    max_tokens: int = 600,
) -> list[OracleTurn]:
    """Keep the most recent PII-scrubbed turns in chronological order within max_tokens."""
    if not history or max_tokens <= 0:
        return []
    kept_reversed: list[OracleTurn] = []
    used = 0
    for turn in reversed(history):
        scrubbed_text = scrub_pii_and_secrets(turn.text.strip())
        if not scrubbed_text:
            continue
        cost = approx_tokens(scrubbed_text) + 4
        if kept_reversed and used + cost > max_tokens:
            break
        if not kept_reversed and cost > max_tokens:
            scrubbed_text = scrubbed_text[: max_tokens * 4]
        kept_reversed.append(OracleTurn(role=turn.role, text=scrubbed_text))
        used += cost
    return list(reversed(kept_reversed))


def _meaningful_code_lines(code: str) -> set[str]:
    lines: set[str] = set()
    for raw in code.splitlines():
        stripped = " ".join(raw.strip().split())
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith(("import ", "from ", "def ", "async def ", "class ")):
            continue
        lines.add(stripped)
    return lines


def enforce_output_spoiler_firewall(
    answer: str,
    solution_files: dict[str, str],
) -> tuple[str, bool]:
    """Redact fenced code blocks from LLM replies if they leak >= 70% of a solution file."""
    if not answer or not solution_files:
        return answer, False

    sol_line_sets = [
        lines
        for code in solution_files.values()
        if len(lines := _meaningful_code_lines(code)) >= 3
    ]
    if not sol_line_sets:
        return answer, False

    triggered = False

    def _replace_if_spoiler(match: re.Match[str]) -> str:
        nonlocal triggered
        block_lines = _meaningful_code_lines(match.group(1))
        if len(block_lines) < 3:
            return match.group(0)
        for sol_lines in sol_line_sets:
            overlap = len(block_lines & sol_lines)
            coverage = overlap / len(sol_lines)
            if overlap >= 3 and coverage >= 0.70:
                triggered = True
                return (
                    "```python\n"
                    "# [Socratic Firewall: Full solution redacted — focus on the guided step above]\n"
                    "```"
                )
        return match.group(0)

    filtered = _FENCED_BLOCK_RE.sub(_replace_if_spoiler, answer)
    return filtered, triggered


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
