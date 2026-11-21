from flask_service import create_app


def test_flask_health_and_blueprint_crud() -> None:
    app = create_app()
    client = app.test_client()

    health = client.get("/health")
    assert health.status_code == 200
    assert health.get_json() == {"status": "ok"}

    created = client.post("/api/items", json={"name": "  rack-unit ", "qty": 4})
    assert created.status_code == 201
    item = created.get_json()
    assert item == {"id": 1, "name": "rack-unit", "qty": 4}

    fetched = client.get("/api/items/1")
    assert fetched.status_code == 200
    assert fetched.get_json() == item


def test_flask_validation_and_json_404_handler() -> None:
    app = create_app()
    client = app.test_client()

    bad = client.post("/api/items", json={"name": "  ", "qty": 2})
    assert bad.status_code == 400

    bad_bool = client.post("/api/items", json={"name": "widget", "qty": True})
    assert bad_bool.status_code == 400

    missing = client.get("/api/items/999")
    assert missing.status_code == 404
    assert "error" in missing.get_json()

    unknown_route = client.get("/nope")
    assert unknown_route.status_code == 404
    assert unknown_route.get_json() == {"error": "not found"}
