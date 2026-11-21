from app import create_app
from fastapi.testclient import TestClient
from security import create_access_token


def test_jwt_401_on_missing_tampered_and_expired_tokens() -> None:
    client = TestClient(create_app())

    assert client.get("/me").status_code == 401
    assert client.get("/me", headers={"Authorization": "Bearer bad.jwt.tok"}).status_code == 401

    expired = create_access_token("u1", "viewer", ttl_seconds=-10)
    assert client.get("/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_rbac_returns_403_for_viewer_and_200_for_admin() -> None:
    client = TestClient(create_app())
    viewer_tok = create_access_token("u-viewer", "viewer")
    admin_tok = create_access_token("u-admin", "admin")

    me = client.get("/me", headers={"Authorization": f"Bearer {viewer_tok}"})
    assert me.status_code == 200
    assert me.json() == {"sub": "u-viewer", "role": "viewer"}

    denied = client.get("/admin/audit", headers={"Authorization": f"Bearer {viewer_tok}"})
    assert denied.status_code == 403

    allowed = client.get("/admin/audit", headers={"Authorization": f"Bearer {admin_tok}"})
    assert allowed.status_code == 200
    assert allowed.json() == {"audit": "ok", "actor": "u-admin"}
