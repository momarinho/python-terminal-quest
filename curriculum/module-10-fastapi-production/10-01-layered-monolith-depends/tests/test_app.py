from app import create_app, get_repo
from domain import InMemoryTicketRepo
from fastapi.testclient import TestClient


def test_tickets_crud_with_dependency_override() -> None:
    app = create_app()
    fake_repo = InMemoryTicketRepo()
    app.dependency_overrides[get_repo] = lambda: fake_repo

    client = TestClient(app)
    created = client.post("/tickets", json={"title": "  Fix cache ", "priority": 1})
    assert created.status_code == 201
    data = created.get_json() if hasattr(created, "get_json") else created.json()
    assert data == {"id": "tkt-1", "title": "Fix cache", "priority": 1}

    fetched = client.get("/tickets/tkt-1")
    assert fetched.status_code == 200
    assert fetched.json() == data


def test_missing_ticket_and_invalid_priority() -> None:
    app = create_app()
    app.dependency_overrides[get_repo] = lambda: InMemoryTicketRepo()
    client = TestClient(app)

    assert client.get("/tickets/missing").status_code == 404
    assert client.post("/tickets", json={"title": "ok", "priority": 99}).status_code == 422
