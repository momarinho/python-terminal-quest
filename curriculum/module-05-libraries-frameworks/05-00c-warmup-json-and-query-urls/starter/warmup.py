import json  # noqa: F401
from urllib.parse import urlencode  # noqa: F401


def decode_status(raw_json: str) -> str:
    """Parse JSON string and return 'status' field or 'unknown'."""
    return ""


def build_query_url(base_url: str, params: dict[str, str]) -> str:
    """Encode params dict as a URL query string attached to base_url."""
    return base_url
