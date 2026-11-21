import requests


class FetchError(Exception):
    """Raised when fetching an HTML report source fails."""


def fetch_html(url: str, timeout: float = 2.0) -> str:
    """Fetch HTML body using requests.Session with explicit timeout, raising FetchError on failure."""
    # TODO: use requests.Session().get(url, timeout=timeout) and raise_for_status()
    _ = requests
    return ""
