from warmup import clean_label, is_enabled, parse_count


def test_clean_label() -> None:
    assert clean_label("  API_Gateway ") == "api_gateway"


def test_parse_count() -> None:
    assert parse_count("  42 ") == 42


def test_is_enabled() -> None:
    assert is_enabled(" YES ") is True
    assert is_enabled("false") is False
