from types import TracebackType

import requests


class HttpClientError(Exception):
    """Raised when an HTTP request fails permanently or exhausts retries."""


class ApiGatewayClient:
    _RETRYABLE_STATUSES = {502, 503, 504}

    def __init__(
        self,
        base_url: str,
        timeout: float = 2.0,
        user_agent: str = "pyquest-client/1.0",
        max_retries: int = 1,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": user_agent,
            }
        )

    def fetch_json(self, path: str) -> dict[str, object]:
        """GET `<base_url>/<path>`, retrying on Timeout or 502/503/504, raising HttpClientError on failure."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        attempts = self.max_retries + 1

        for attempt in range(1, attempts + 1):
            try:
                resp = self._session.get(url, timeout=self.timeout)
            except requests.RequestException as exc:
                if isinstance(exc, requests.Timeout) and attempt < attempts:
                    continue
                raise HttpClientError(f"Request failed for {url}: {exc}") from exc

            if resp.status_code in self._RETRYABLE_STATUSES and attempt < attempts:
                continue

            try:
                resp.raise_for_status()
                data = resp.json()
            except (requests.HTTPError, ValueError) as exc:
                raise HttpClientError(f"HTTP error {resp.status_code} at {url}") from exc

            if not isinstance(data, dict):
                raise HttpClientError("Expected JSON object response")
            return data

        raise HttpClientError(f"Exhausted retries for {url}")

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "ApiGatewayClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
