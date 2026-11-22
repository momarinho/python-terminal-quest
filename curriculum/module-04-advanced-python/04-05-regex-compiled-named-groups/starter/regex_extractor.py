import re


def parse_access_entry(line: str) -> dict[str, int | str] | None:
    """Parse '<METHOD> <PATH> -> <STATUS> (<LATENCY>ms)' into typed dict, or None."""
    _ = re
    return None


def mask_bearer_tokens(text: str) -> str:
    """Replace 'Bearer <token>' secrets with 'Bearer [REDACTED]' (preserving original prefix casing)."""
    return text


def extract_trace_tags(log_line: str) -> dict[str, str]:
    """Extract all `key=val` pairs matching `[a-z][a-z0-9_]*=[A-Za-z0-9._:/-]+` via compiled finditer."""
    return {}
