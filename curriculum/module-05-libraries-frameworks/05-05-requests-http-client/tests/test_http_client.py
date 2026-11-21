import json
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from http_client import ApiGatewayClient, HttpClientError


@contextmanager
def _local_test_server() -> Iterator[tuple[str, dict[str, int | str]]]:
    state: dict[str, int | str] = {"flaky_calls": 0, "user_agent": ""}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

        def do_GET(self) -> None:
            state["user_agent"] = self.headers.get("User-Agent", "")
            if self.path == "/flaky":
                state["flaky_calls"] = int(state["flaky_calls"]) + 1
                if int(state["flaky_calls"]) == 1:
                    self.send_response(503)
                    self.end_headers()
                    return
                body = json.dumps({"ok": True, "attempt": state["flaky_calls"]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/slow":
                time.sleep(0.35)
                self.send_response(200)
                self.end_headers()
                return

            self.send_response(404)
            self.end_headers()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        yield f"http://{host}:{port}", state
    finally:
        server.shutdown()
        server.server_close()


def test_retries_503_and_sends_custom_headers() -> None:
    with _local_test_server() as (base_url, state):
        client = ApiGatewayClient(base_url, timeout=1.0, user_agent="pyquest-agent/2", max_retries=1)
        try:
            data = client.fetch_json("/flaky")
            assert data == {"ok": True, "attempt": 2}
            assert state["user_agent"] == "pyquest-agent/2"
        finally:
            client.close()


def test_raises_http_client_error_on_404_and_timeout() -> None:
    with _local_test_server() as (base_url, _state):
        client = ApiGatewayClient(base_url, timeout=0.1, max_retries=0)
        try:
            with pytest.raises(HttpClientError):
                client.fetch_json("/missing")
            with pytest.raises(HttpClientError):
                client.fetch_json("/slow")
        finally:
            client.close()
