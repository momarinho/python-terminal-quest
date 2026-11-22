import re

_ACCESS_LOG_RE = re.compile(
    r"^(?P<method>GET|POST|PUT|DELETE|PATCH)\s+(?P<path>/\S*)\s+->\s+(?P<status>\d{3})\s+\((?P<latency_ms>\d+)ms\)$"
)
_BEARER_RE = re.compile(r"\b(Bearer)\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
_TRACE_TAG_RE = re.compile(r"(?P<key>[a-z][a-z0-9_]*)=(?P<val>[A-Za-z0-9._:/-]+)")


def parse_access_entry(line: str) -> dict[str, int | str] | None:
    """Parse '<METHOD> <PATH> -> <STATUS> (<LATENCY>ms)' into typed dict, or None."""
    match = _ACCESS_LOG_RE.fullmatch(line.strip())
    if not match:
        return None
    groups = match.groupdict()
    return {
        "method": groups["method"],
        "path": groups["path"],
        "status": int(groups["status"]),
        "latency_ms": int(groups["latency_ms"]),
    }


def mask_bearer_tokens(text: str) -> str:
    """Replace 'Bearer <token>' secrets with 'Bearer [REDACTED]' (preserving original prefix casing)."""
    return _BEARER_RE.sub(lambda m: f"{m.group(1)} [REDACTED]", text)


def extract_trace_tags(log_line: str) -> dict[str, str]:
    """Extract all `key=val` pairs matching `[a-z][a-z0-9_]*=[A-Za-z0-9._:/-]+` via compiled finditer."""
    return {m.group("key"): m.group("val") for m in _TRACE_TAG_RE.finditer(log_line)}
