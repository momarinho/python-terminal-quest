from warmup import estimate_tokens, keyword_overlap_score, redact_api_key


def test_estimate_tokens() -> None:
    assert estimate_tokens("") == 0
    assert estimate_tokens("hello") == 2


def test_redact_api_key() -> None:
    cleaned = redact_api_key("Using key sk-AbCdEf12345 in request")
    assert cleaned == "Using key [REDACTED] in request"


def test_keyword_overlap_score() -> None:
    score = keyword_overlap_score("async fastapi depends", "FastAPI Depends injection guide")
    assert round(score, 2) == 0.67
    assert keyword_overlap_score("", "anything") == 0.0
