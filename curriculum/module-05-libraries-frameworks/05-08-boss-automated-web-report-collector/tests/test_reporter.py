import threading
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import matplotlib.pyplot as plt
import pytest
from fetcher import FetchError
from parser import parse_metrics_table
from reporter import build_report

HTML_FIXTURE = """
<html><body>
  <table id="metrics">
    <tbody>
      <tr><td>us-east</td><td>auth</td><td>20</td></tr>
      <tr><td>us-east</td><td>billing</td><td>40</td></tr>
      <tr><td>eu-west</td><td>auth</td><td>55</td></tr>
      <tr><td>bad-row</td><td>x</td><td>not-a-num</td></tr>
    </tbody>
  </table>
</body></html>
"""


@contextmanager
def _serve_html() -> Iterator[str]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

        def do_GET(self) -> None:
            if self.path == "/metrics.html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(HTML_FIXTURE.encode("utf-8"))
                return
            self.send_response(404)
            self.end_headers()

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = srv.server_address
        yield f"http://{host}:{port}"
    finally:
        srv.shutdown()
        srv.server_close()


def test_parse_metrics_table_skips_invalid_rows() -> None:
    rows = parse_metrics_table(HTML_FIXTURE)
    assert rows == [
        {"region": "us-east", "service": "auth", "latency_ms": 20},
        {"region": "us-east", "service": "billing", "latency_ms": 40},
        {"region": "eu-west", "service": "auth", "latency_ms": 55},
    ]


def test_build_report_end_to_end_offline(tmp_path: Path) -> None:
    before_figs = set(plt.get_fignums())
    chart_path = tmp_path / "out" / "latency.png"
    report_path = tmp_path / "out" / "digest.md"

    with _serve_html() as base_url:
        df = build_report(f"{base_url}/metrics.html", chart_path, report_path)

        assert list(df["region"]) == ["eu-west", "us-east"]
        assert list(df["avg_latency_ms"]) == [55.0, 30.0]
        assert list(df["service_count"]) == [1, 2]

        assert chart_path.exists()
        assert chart_path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        assert set(plt.get_fignums()) == before_figs

        md = report_path.read_text(encoding="utf-8")
        assert "eu-west" in md and "55.00" in md
        assert "us-east" in md and "30.00" in md

        with pytest.raises(FetchError):
            build_report(f"{base_url}/missing", chart_path, report_path)
