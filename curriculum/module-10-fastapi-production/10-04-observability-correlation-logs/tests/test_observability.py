from app import create_app
from fastapi.testclient import TestClient
from observability import REQUEST_ID_CTX, MetricsRegistry


def test_correlation_id_propagation_and_contextvar_reset() -> None:
    logs: list[dict[str, object]] = []
    registry = MetricsRegistry()
    client = TestClient(create_app(log_sink=logs, metrics=registry))

    r1 = client.get("/work", headers={"X-Request-ID": "req-abc-123"})
    assert r1.status_code == 200
    assert r1.headers["X-Request-ID"] == "req-abc-123"
    assert r1.json() == {"request_id": "req-abc-123"}
    assert REQUEST_ID_CTX.get() is None

    r2 = client.get("/work")
    assert r2.status_code == 200
    assert r2.headers["X-Request-ID"]
    assert r2.headers["X-Request-ID"] != "req-abc-123"


def test_structured_logs_and_metrics_snapshot() -> None:
    logs: list[dict[str, object]] = []
    registry = MetricsRegistry()
    client = TestClient(create_app(log_sink=logs, metrics=registry))

    client.get("/work", headers={"X-Request-ID": "trace-1"})
    client.get("/boom", headers={"X-Request-ID": "trace-2"})

    assert len(logs) == 2
    assert logs[0]["request_id"] == "trace-1"
    assert logs[0]["status_code"] == 200
    assert logs[1]["status_code"] == 500

    snap = client.get("/metrics").json()
    assert snap["requests_total"] == 2
    assert snap["errors_total"] == 1
