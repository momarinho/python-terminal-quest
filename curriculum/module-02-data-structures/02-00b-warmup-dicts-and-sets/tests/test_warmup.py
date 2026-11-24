from warmup import safe_lookup, unique_sorted_tags


def test_safe_lookup() -> None:
    assert safe_lookup({"ada": 95}, "ada") == 95
    assert safe_lookup({"ada": 95}, "bob") == 0


def test_unique_sorted_tags() -> None:
    assert unique_sorted_tags(["python", "sql", "python", "api"]) == ["api", "python", "sql"]
