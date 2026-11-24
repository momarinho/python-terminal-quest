from fastapi.testclient import TestClient
from warmup import app, get_user_store

client = TestClient(app)


def test_get_user_and_404() -> None:
    assert client.get("/users/alice").json() == {"username": "alice", "role": "admin"}
    assert client.get("/users/nobody").status_code == 404


def test_depends_override() -> None:
    app.dependency_overrides[get_user_store] = lambda: {"bob": "editor"}
    try:
        resp = client.get("/users/bob")
        assert resp.status_code == 200
        assert resp.json()["role"] == "editor"
    finally:
        app.dependency_overrides.clear()
