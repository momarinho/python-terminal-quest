import re

_EMAIL_RE = re.compile(r"\b([A-Za-z0-9._%+-])([A-Za-z0-9._%+-]*)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
_CPF_RE = re.compile(r"\b\d{3}\.(\d{3}\.\d{3})-\d{2}\b")
_BEARER_RE = re.compile(r"\b(Bearer)\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)


def redact_line(line: str) -> tuple[str, dict[str, int]]:
    """Redact emails, formatted CPFs (***.XXX.YYY-**), and Bearer tokens; return (redacted, counts)."""
    out, email_count = _EMAIL_RE.subn(lambda m: f"{m.group(1)}***@{m.group(3)}", line)
    out, cpf_count = _CPF_RE.subn(lambda m: f"***.{m.group(1)}-**", out)
    out, bearer_count = _BEARER_RE.subn(lambda m: f"{m.group(1)} [REDACTED]", out)
    return out, {
        "emails": email_count,
        "cpfs": cpf_count,
        "bearers": bearer_count,
    }
