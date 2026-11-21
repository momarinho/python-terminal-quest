def extract_bearer_token(auth_header: str) -> str:
    """Extract the token from a 'Bearer <token>' header (case-insensitive scheme)."""
    cleaned = auth_header.strip()
    parts = cleaned.split(None, 1)
    if len(parts) != 2 or parts[0].casefold() != "bearer":
        raise ValueError("Authorization header must start with 'Bearer '")
    token = parts[1].strip()
    if not token:
        raise ValueError("Bearer token must not be empty")
    return token


def parse_kv_log(line: str) -> dict[str, str]:
    """Parse space-separated 'key=value' tokens (preserving '=' inside values and stripping outer quotes)."""
    result: dict[str, str] = {}
    for token in line.strip().split():
        if "=" not in token:
            raise ValueError(f"Malformed key=value token: {token!r}")
        key, val = token.split("=", 1)
        clean_key = key.strip().casefold()
        if not clean_key:
            raise ValueError("Empty key in log line")
        clean_val = val.strip().removeprefix('"').removesuffix('"')
        result[clean_key] = clean_val
    return result


def format_kv_line(fields: dict[str, str]) -> str:
    """Format fields deterministically sorted by key as 'k1=v1 k2=v2'."""
    return " ".join(f"{key}={fields[key]}" for key in sorted(fields))
