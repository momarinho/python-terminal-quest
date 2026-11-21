import requests


class HttpClientError(Exception):
    """Raised when an HTTP request fails permanently or exhausts retries."""


class ApiGatewayClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 2.0,
        user_agent: str = "pyquest-client/1.0",
        max_retries: int = 1,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = requests.Session()
        # TODO: configure default Accept and User-Agent headers on self._session.headers
        _ = user_agent

    def fetch_json(self, path: str) -> dict[str, object]:
        """GET `<base_url>/<path>`, retrying on Timeout or 502/503/504, raising HttpClientError on failure."""
        # TODO: implement request with timeout, retry on transient 5xx/Timeout, raise HttpClientError
        return {}

    def close(self) -> None:
        self._session.close()
