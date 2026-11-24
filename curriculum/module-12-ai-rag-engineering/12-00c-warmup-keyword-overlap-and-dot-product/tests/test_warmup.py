from warmup import dot_product, keyword_overlap


def test_keyword_overlap() -> None:
    score = keyword_overlap("async fastapi depends", "FastAPI Depends guide")
    assert round(score, 2) == 0.67
    assert keyword_overlap("", "text") == 0.0


def test_dot_product() -> None:
    assert dot_product([1.0, 2.0, 3.0], [4.0, 0.5, 2.0]) == 11.0
