import pytest
from deploy_gates import (
    fastest_healthy_region,
    has_blocking_alert,
    is_release_ready,
    rank_endpoints,
)


def test_release_ready_and_blocking_alerts() -> None:
    assert is_release_ready([]) is False
    assert is_release_ready([{"name": "unit", "passed": True}, {"name": "lint", "passed": True}]) is True
    assert is_release_ready([{"name": "unit", "passed": True}, {"name": "lint", "passed": False}]) is False

    assert has_blocking_alert([{"severity": "critical", "acked": True}]) is False
    assert has_blocking_alert([{"severity": "warn", "acked": False}, {"severity": "critical", "acked": False}]) is True


def test_rank_endpoints_does_not_mutate_and_breaks_ties() -> None:
    endpoints = [
        {"path": "/z", "error_rate": 0.05, "p99_ms": 120},
        {"path": "/a", "error_rate": 0.05, "p99_ms": 120},
        {"path": "/fast-fail", "error_rate": 0.12, "p99_ms": 40},
        {"path": "/slow", "error_rate": 0.05, "p99_ms": 300},
    ]
    snapshot = list(endpoints)
    assert rank_endpoints(endpoints) == ["/fast-fail", "/slow", "/a", "/z"]
    assert endpoints == snapshot


def test_fastest_healthy_region() -> None:
    regions = [
        {"name": "ap-south-1", "healthy": False, "latency_ms": 5},
        {"name": "us-east-1", "healthy": True, "latency_ms": 22},
        {"name": "eu-west-1", "healthy": True, "latency_ms": 22},
    ]
    assert fastest_healthy_region(regions) == "eu-west-1"
    with pytest.raises(ValueError):
        fastest_healthy_region([{"name": "us-east-1", "healthy": False, "latency_ms": 10}])
