from app import create_app
from errors import REQUEST_ID_CTX
from fastapi.testclient import TestClient
from security import create_token


def test_gateway_auth_rbac_rfc7807_and_correlation() -> None:
    logs: list[dict[str, object]] = []
    client = TestClient(create_app(audit_sink=logs))

    assert client.get("/health").json() == {"status": "ok"}

    unauth = client.post(
        "/admin/policies",
        json={"policy_id": "p1", "rate_limit": 100},
        headers={"X-Request-ID": "trace-401"},
    )
    assert unauth.status_code == 401
    assert unauth.headers["content-type"].startswith("application/problem+json")
    assert unauth.headers["X-Request-ID"] == "trace-401"
    assert unauth.json()["request_id"] == "trace-401"

    auditor_tok = create_token("aud-1", "auditor")
    admin_tok = create_token("adm-1", "admin")

    forbidden = client.post(
        "/admin/policies",
        json={"policy_id": "p1", "rate_limit": 100},
        headers={"Authorization": f"Bearer {auditor_tok}"},
    )
    assert forbidden.status_code == 403
    assert forbidden.json()["type"] == "urn:gateway:forbidden"

    created = client.post(
        "/admin/policies",
        json={"policy_id": "p1", "rate_limit": 100},
        headers={"Authorization": f"Bearer {admin_tok}", "X-Request-ID": "trace-201"},
    )
    assert created.status_code == 201
    assert created.json()["created_by"] == "adm-1"
    assert created.json()["request_id"] == "trace-201"

    fetched = client.get(
        "/admin/policies/p1",
        headers={"Authorization": f"Bearer {auditor_tok}"},
    )
    assert fetched.status_code == 200
    assert REQUEST_ID_CTX.get() is None
    assert len(logs) == 5


def test_gateway_conflict_not_found_and_validation_rfc7807() -> None:
    client = TestClient(create_app())
    admin_tok = create_token("adm-1", "admin")
    headers = {"Authorization": f"Bearer {admin_tok}"}

    assert client.post("/admin/policies", json={"policy_id": "p1", "rate_limit": 50}, headers=headers).status_code == 201
    assert client.post("/admin/policies", json={"policy_id": "p1", "rate_limit": 50}, headers=headers).status_code == 409
    assert client.get("/admin/policies/missing", headers=headers).status_code == 404

    invalid = client.post("/admin/policies", json={"policy_id": "x", "rate_limit": 0}, headers=headers)
    assert invalid.status_code == 422
    assert invalid.json()["type"] == "urn:gateway:validation-error"
