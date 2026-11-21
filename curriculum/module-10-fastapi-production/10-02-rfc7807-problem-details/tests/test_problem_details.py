from app import create_app
from fastapi.testclient import TestClient


def test_domain_errors_return_rfc7807_problem_json() -> None:
    client = TestClient(create_app())

    r1 = client.post("/orders", json={"order_id": "ord-1", "amount_cents": 500})
    assert r1.status_code == 201

    dup = client.post("/orders", json={"order_id": "ord-1", "amount_cents": 500})
    assert dup.status_code == 409
    assert dup.headers["content-type"].startswith("application/problem+json")
    assert dup.json()["type"] == "urn:problem:conflict"
    assert dup.json()["instance"] == "/orders"

    missing = client.get("/orders/nope")
    assert missing.status_code == 404
    assert missing.json()["type"] == "urn:problem:not-found"

    forbidden = client.get("/orders/secret")
    assert forbidden.status_code == 403
    assert forbidden.json()["type"] == "urn:problem:forbidden"


def test_validation_error_returns_rfc7807_with_errors_list() -> None:
    client = TestClient(create_app())
    bad = client.post("/orders", json={"order_id": "x", "amount_cents": -10})
    assert bad.status_code == 422
    assert bad.headers["content-type"].startswith("application/problem+json")
    body = bad.json()
    assert body["type"] == "urn:problem:validation-error"
    assert len(body["errors"]) == 1
