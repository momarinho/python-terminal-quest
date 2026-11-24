from fastapi.testclient import TestClient
from warmup import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_read_item_path_and_query() -> None:
    resp = client.get("/items/42?tag=urgent")
    assert resp.status_code == 200
    assert resp.json() == {"item_id": 42, "tag": "urgent"}
