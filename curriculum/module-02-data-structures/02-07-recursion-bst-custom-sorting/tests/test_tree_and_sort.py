from tree_and_sort import MetricBST, collect_transitive_deps, sort_services


def test_collect_transitive_deps_handles_cycles() -> None:
    graph = {
        "api": ["auth", "billing"],
        "auth": ["redis", "pg"],
        "billing": ["pg", "api"],
        "redis": [],
        "pg": [],
    }
    assert collect_transitive_deps(graph, "api") == ["auth", "billing", "pg", "redis"]


def test_metric_bst_insert_contains_inorder() -> None:
    bst = MetricBST()
    for val in [50, 20, 75, 10, 35, 20, 90]:
        bst.insert(val)
    assert bst.inorder() == [10, 20, 35, 50, 75, 90]
    assert bst.contains(35) is True
    assert bst.contains(42) is False


def test_sort_services_multi_key() -> None:
    services = [
        {"name": "zeta", "tier": 2, "latency_ms": 15},
        {"name": "alpha", "tier": 2, "latency_ms": 15},
        {"name": "core", "tier": 3, "latency_ms": 40},
        {"name": "fast", "tier": 2, "latency_ms": 5},
    ]
    ordered = [s["name"] for s in sort_services(services)]
    assert ordered == ["core", "fast", "alpha", "zeta"]
