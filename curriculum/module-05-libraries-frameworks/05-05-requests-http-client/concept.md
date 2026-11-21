## Concept: Resilient HTTP Clients with `requests.Session`

Calling bare `requests.get(url)` without `timeout=` can hang a worker thread forever if a remote host stalls! Production clients always enforce timeouts, reuse TCP connections via `requests.Session`, and classify transient vs. permanent HTTP failures.

### `requests.Session` & `raise_for_status()`
```python
import requests

class CatalogClientError(Exception):
    pass

def fetch_station_json(base_url: str, station_id: str, timeout: float = 2.0) -> dict[str, object]:
    with requests.Session() as session:
        session.headers.update({"Accept": "application/json"})
        resp = session.get(f"{base_url.rstrip('/')}/stations/{station_id}", timeout=timeout)
        resp.raise_for_status()
        return resp.json()
```

### Challenge
Implement `HttpClientError` and `ApiGatewayClient` (using `requests.Session` with default `User-Agent` and `Accept: application/json` headers, explicit `timeout`, `close()` / context manager support, and `fetch_json(path)` retrying once on `503` or `requests.Timeout` up to `max_retries`) in `http_client.py`.
