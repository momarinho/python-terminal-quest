import asyncio

from warmup import fetch_all_tags, fetch_tag


def test_fetch_tag() -> None:
    assert asyncio.run(fetch_tag("py")) == "PY"


def test_fetch_all_tags() -> None:
    assert asyncio.run(fetch_all_tags(["api", "db", "rag"])) == ["API", "DB", "RAG"]
