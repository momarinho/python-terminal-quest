from html_extractor import extract_nav_links, extract_service_table

SAMPLE_HTML = """
<html>
  <body>
    <nav>
      <a href=" /docs "> Docs </a>
      <a href="">Empty</a>
      <a>NoHref</a>
      <a href="/status"><span>System</span> Status</a>
    </nav>
    <table id="status-table">
      <thead><tr><th>Service</th><th>Status</th><th>Latency</th></tr></thead>
      <tbody>
        <tr><td> auth-api </td><td>healthy</td><td> 18ms </td></tr>
        <tr><td>broken-row</td></tr>
        <tr><td>billing</td><td>degraded</td><td>142</td></tr>
      </tbody>
    </table>
  </body>
</html>
"""


def test_extract_service_table_handles_whitespace_and_bad_rows() -> None:
    assert extract_service_table(SAMPLE_HTML) == [
        {"service": "auth-api", "status": "HEALTHY", "latency_ms": 18},
        {"service": "billing", "status": "DEGRADED", "latency_ms": 142},
    ]


def test_extract_nav_links_filters_missing_or_empty_href() -> None:
    assert extract_nav_links(SAMPLE_HTML) == [
        {"label": "Docs", "href": "/docs"},
        {"label": "System Status", "href": "/status"},
    ]
