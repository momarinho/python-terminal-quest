import re


def parse_access_entry(line: str) -> dict[str, int | str] | None:
    """Parse '<METHOD> <PATH> -> <STATUS> (<LATENCY>ms)' into typed dict, or None."""
    # TODO: use a compiled regex with named groups (?P<method>...), (?P<path>...), (?P<status>...), (?P<latency_ms>...)
    _ = re
    return None


def mask_bearer_tokens(text: str) -> str:
    """Replace 'Bearer <token>' secrets with 'Bearer [REDACTED]' (case-insensitive prefix)."""
    # TODO: compile pattern and use re.sub
    return text
