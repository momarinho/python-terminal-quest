import pytest
from kv_log_parser import extract_bearer_token, format_kv_line, parse_kv_log


def test_extract_bearer_token_preserves_bearer_chars_in_token() -> None:
    assert extract_bearer_token("Bearer abc123==") == "abc123=="
    assert extract_bearer_token("  bearer   earring_token ") == "earring_token"
    with pytest.raises(ValueError):
        extract_bearer_token("Basic dXNlcjpwYXNz")
    with pytest.raises(ValueError):
        extract_bearer_token("Bearer   ")


def test_parse_kv_log_preserves_equals_in_values() -> None:
    parsed = parse_kv_log('LEVEL=info path="/v1/pay?a=1&b=2" sig=xyz==')
    assert parsed == {
        "level": "info",
        "path": "/v1/pay?a=1&b=2",
        "sig": "xyz==",
    }
    with pytest.raises(ValueError):
        parse_kv_log("level=info broken_token")


def test_format_kv_line_deterministic_order() -> None:
    assert format_kv_line({"status": "503", "service": "auth"}) == "service=auth status=503"
