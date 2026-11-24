from fastapi.testclient import TestClient
from warmup import app, get_app_version

client = TestClient(app)


def test_ping_uses_depends() -> None:
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json() == {"status": "pong", "version": "1.0.0"}

    app.dependency_overrides[get_app_version] = lambda: "2.0.0-test"
    try:
        override_resp = client.get("/ping")
        assert override_resp.json()["version"] == "2.0.0-test"
    finally:
        app.dependency_overrides.clear()


def test_echo_returns_201() -> None:
    resp = client.post("/echo", json={"message": "  hello fastapi  "})
    assert resp.status_code == 201
    assert resp.json() == {"echo": "hello fastapi"}
