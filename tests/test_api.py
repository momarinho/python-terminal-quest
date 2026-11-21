from pathlib import Path

from fastapi.testclient import TestClient

from pyquest.api.app import create_app
from pyquest.config import Settings

REPO_ROOT = Path(__file__).resolve().parents[1]


def _make_client(tmp_path: Path) -> TestClient:
    settings = Settings(
        db_path=tmp_path / "progress.db",
        curriculum_dir=REPO_ROOT / "curriculum",
        web_dist_dir=tmp_path / "missing_dist",
    )
    return TestClient(create_app(settings))


def test_health_and_curriculum_endpoints(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert health.json()["lessons"] == 17

    curr = client.get("/api/curriculum")
    assert curr.status_code == 200
    body = curr.json()
    assert body["totalLessons"] == 17
    assert body["completedLessons"] == 0
    assert body["hero"]["tier"] == 1
    assert body["hero"]["title"] == "Apprentice"
    assert len(body["modules"]) == 2


def test_lesson_run_draft_notes_flag_reset_and_oracle(tmp_path: Path) -> None:
    client = _make_client(tmp_path)

    # Multi-file Boss Fight lesson 01-09
    lesson_resp = client.get("/api/lessons/01-09")
    assert lesson_resp.status_code == 200
    lesson_data = lesson_resp.json()
    assert set(lesson_data["files"].keys()) == {"models.py", "engine.py"}

    # Save multi-file draft
    draft_files = {
        "models.py": lesson_data["files"]["models.py"] + "\n# learner note\n",
        "engine.py": lesson_data["files"]["engine.py"],
    }
    draft_resp = client.post("/api/lessons/01-09/draft", json={"files": draft_files})
    assert draft_resp.status_code == 200
    assert "# learner note" in client.get("/api/lessons/01-09").json()["files"]["models.py"]

    # Notes & Flag
    notes_resp = client.post("/api/lessons/01-09/notes", json={"notes": "Remember Decimal('0.01')"})
    assert notes_resp.status_code == 200
    assert notes_resp.json()["notes"] == "Remember Decimal('0.01')"

    flag_resp = client.post("/api/lessons/01-09/flag", json={"flagged": True})
    assert flag_resp.status_code == 200
    assert flag_resp.json()["flagged"] is True

    # Run with solution passes and updates XP & streak
    sol_files = client.get("/api/lessons/01-09/solution").json()["files"]
    run_resp = client.post("/api/lessons/01-09/run", json={"files": sol_files})
    assert run_resp.status_code == 200
    run_body = run_resp.json()
    assert run_body["result"]["passed"] is True
    assert run_body["progress"]["status"] == "COMPLETED"
    assert run_body["hero"]["earnedXp"] == 250

    # Oracle ask endpoint
    oracle_resp = client.post(
        "/api/oracle/ask",
        json={
            "lessonId": "01-09",
            "question": "Why should I use Decimal instead of float?",
            "files": sol_files,
        },
    )
    assert oracle_resp.status_code == 200
    oracle_body = oracle_resp.json()
    assert oracle_body["provider"] == "stub-local"
    assert "Decimal" in oracle_body["answer"]

    # Reset restores starter files
    reset_resp = client.post("/api/lessons/01-09/reset")
    assert reset_resp.status_code == 200
    assert "# learner note" not in reset_resp.json()["files"]["models.py"]


def test_projects_endpoint(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    data = resp.json()
    assert data["totalProjects"] >= 1
    assert data["projects"][0]["id"] == "proj-01-ledger-reconciler"
