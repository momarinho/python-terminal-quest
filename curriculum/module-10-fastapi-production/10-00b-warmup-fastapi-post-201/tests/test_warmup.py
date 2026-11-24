from fastapi.testclient import TestClient
from warmup import app

client = TestClient(app)


def test_create_note_returns_201() -> None:
    resp = client.post("/notes", json={"title": "  Review indexes  "})
    assert resp.status_code == 201
    assert resp.json() == {"title": "Review indexes"}


def test_create_note_missing_field_422() -> None:
    resp = client.post("/notes", json={})
    assert resp.status_code == 422
