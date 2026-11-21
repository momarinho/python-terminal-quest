def extract_bearer_token(auth_header: str) -> str:
    """Extract the token from a 'Bearer <token>' header (case-insensitive scheme)."""
    # TODO: reject missing/non-Bearer headers with ValueError; preserve leading 'B'/'e'/'a'/'r' in token!
    return auth_header.lstrip("Bearer ").strip()  # noqa: B005


def parse_kv_log(line: str) -> dict[str, str]:
    """Parse space-separated 'key=value' tokens (preserving '=' inside values and stripping outer quotes)."""
    # TODO: split tokens, split each on '=' with maxsplit=1, normalize key lowercase
    return {}


def format_kv_line(fields: dict[str, str]) -> str:
    """Format fields deterministically sorted by key as 'k1=v1 k2=v2'."""
    # TODO: use sorted items and str.join
    return ""
