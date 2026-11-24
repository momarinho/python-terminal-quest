import json
from urllib.parse import urlencode


def decode_status(raw_json: str) -> str:
    """Parse JSON string and return 'status' field or 'unknown'."""
    data = json.loads(raw_json)
    return str(data.get("status", "unknown"))


def build_query_url(base_url: str, params: dict[str, str]) -> str:
    """Encode params dict as a URL query string attached to base_url."""
    return f"{base_url}?{urlencode(params)}"
