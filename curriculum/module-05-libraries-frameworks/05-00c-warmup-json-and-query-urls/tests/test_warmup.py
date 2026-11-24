from warmup import build_query_url, decode_status


def test_decode_status() -> None:
    assert decode_status('{"status": "healthy"}') == "healthy"
    assert decode_status("{}") == "unknown"


def test_build_query_url() -> None:
    url = build_query_url("https://api.example.com/items", {"page": "2", "tag": "py"})
    assert url == "https://api.example.com/items?page=2&tag=py"
