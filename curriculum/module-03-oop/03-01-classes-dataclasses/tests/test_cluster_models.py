from dataclasses import FrozenInstanceError

import pytest
from cluster_models import ClusterSnapshot, ServiceEndpoint


def test_service_endpoint_is_frozen_and_validated() -> None:
    ep = ServiceEndpoint("  auth-api ", 8443, healthy=True, latency_ms=12)
    assert ep.name == "auth-api"
    with pytest.raises(FrozenInstanceError):
        ep.port = 9000  # type: ignore[misc]

    with pytest.raises(ValueError):
        ServiceEndpoint("   ", 8080)
    with pytest.raises(ValueError):
        ServiceEndpoint("api", 70000)
    with pytest.raises(ValueError):
        ServiceEndpoint("api", 8080, latency_ms=-1)


def test_cluster_snapshot_isolated_lists_and_ratio() -> None:
    c1 = ClusterSnapshot("us-east-1")
    c2 = ClusterSnapshot("eu-west-1")
    assert c1.healthy_ratio() == 0.0

    c1.register(ServiceEndpoint("web", 8080, healthy=True))
    c1.register(ServiceEndpoint("worker", 9000, healthy=False))
    assert c1.healthy_ratio() == 0.5
    assert c2.endpoints == []
