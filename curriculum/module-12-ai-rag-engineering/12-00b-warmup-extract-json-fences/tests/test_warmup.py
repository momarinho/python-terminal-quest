import pytest
from warmup import parse_llm_json


def test_parse_fenced_json() -> None:
    noisy = 'Sure! Here is the summary:\n```json\n{"status": "ok", "count": 3}\n```'
    assert parse_llm_json(noisy) == {"status": "ok", "count": 3}


def test_parse_missing_braces_raises() -> None:
    with pytest.raises(ValueError):
        parse_llm_json("No json here")
