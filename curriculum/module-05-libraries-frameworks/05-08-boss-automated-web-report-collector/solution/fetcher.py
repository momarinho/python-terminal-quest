import requests


class FetchError(Exception):
    """Raised when fetching an HTML report source fails."""


def fetch_html(url: str, timeout: float = 2.0) -> str:
    """Fetch HTML body using requests.Session with explicit timeout, raising FetchError on failure."""
    with requests.Session() as session:
        session.headers.update({"User-Agent": "pyquest-collector/1.0"})
        try:
            resp = session.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            raise FetchError(f"Failed to fetch {url}: {exc}") from exc
