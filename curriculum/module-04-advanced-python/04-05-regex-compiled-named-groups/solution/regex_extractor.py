import re

_ACCESS_LOG_RE = re.compile(
    r"^(?P<method>GET|POST|PUT|DELETE|PATCH)\s+(?P<path>/\S*)\s+->\s+(?P<status>\d{3})\s+\((?P<latency_ms>\d+)ms\)$"
)
_BEARER_RE = re.compile(r"\b(Bearer)\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)


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
    """Replace 'Bearer <token>' secrets with 'Bearer [REDACTED]' (case-insensitive prefix)."""
    return _BEARER_RE.sub(lambda m: f"{m.group(1)} [REDACTED]", text)
