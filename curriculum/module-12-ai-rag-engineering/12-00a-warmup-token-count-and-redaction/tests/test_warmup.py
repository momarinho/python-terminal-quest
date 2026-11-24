from warmup import estimate_tokens, redact_api_key


def test_estimate_tokens() -> None:
    assert estimate_tokens("") == 0
    assert estimate_tokens("hello") == 2


def test_redact_api_key() -> None:
    assert redact_api_key("Header sk-Secret123456!") == "Header [REDACTED]!"
