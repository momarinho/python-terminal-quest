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
    assert health.json()["modules"] == 12
    assert health.json()["lessons"] == 75

    curr = client.get("/api/curriculum")
    assert curr.status_code == 200
    body = curr.json()
    assert body["totalLessons"] == 75
    assert body["completedLessons"] == 0
    assert body["hero"]["tier"] == 1
    assert body["hero"]["title"] == "Apprentice"
    assert len(body["modules"]) == 12


def test_lesson_run_draft_notes_flag_reset_and_oracle(tmp_path: Path) -> None:
    client = _make_client(tmp_path)

    # Multi-file Boss Fight lesson 01-09
    lesson_resp = client.get("/api/lessons/01-09")
    assert lesson_resp.status_code == 200
    lesson_data = lesson_resp.json()
    assert set(lesson_data["files"].keys()) == {"models.py", "engine.py"}
    assert len(lesson_data["testFiles"]) >= 1

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

    # DIY RAG Capstone Stub Oracle ask endpoint
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
    assert oracle_body["mode"] == "stub"
    assert oracle_body["provider"] == "stub"
    assert oracle_body["guardrailTriggered"] is False
    assert oracle_body["citations"][0]["lessonId"] == "01-09"
    assert "CAPSTONE_README.md" in oracle_body["answer"]

    # Reset restores starter files
    reset_resp = client.post("/api/lessons/01-09/reset")
    assert reset_resp.status_code == 200
    assert "# learner note" not in reset_resp.json()["files"]["models.py"]


def test_projects_endpoint(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    data = resp.json()
    assert data["totalProjects"] == 3
    assert [p["id"] for p in data["projects"]] == [
        "proj-01-cli-ledger-reconciler",
        "proj-02-inventory-audit-service",
        "proj-03-mini-sidekiq-ai-triage",
    ]
    assert [p["requiredModulesCompleted"] for p in data["projects"]] == [5, 9, 12]
    assert all(not p["milestoneUnlocked"] for p in data["projects"])


def test_solution_reveal_review_reset_and_backup_roundtrip(tmp_path: Path) -> None:
    client = _make_client(tmp_path)

    # Revealing solution before completion marks solutionRevealed=True
    sol_resp = client.get("/api/lessons/01-01/solution")
    assert sol_resp.status_code == 200
    sol_files = sol_resp.json()["files"]

    # Completing after reveal sets needsReview=True
    run_resp = client.post("/api/lessons/01-01/run", json={"files": sol_files})
    assert run_resp.status_code == 200
    prog = run_resp.json()["progress"]
    assert prog["status"] == "COMPLETED"
    assert prog["solutionRevealed"] is True
    assert prog["needsReview"] is True
    assert prog["completedAt"] != ""

    # Export backup, then import into a fresh DB
    client.post("/api/lessons/01-01/notes", json={"notes": "Backup note check"})
    export_resp = client.get("/api/progress/export")
    assert export_resp.status_code == 200
    backup_payload = export_resp.json()
    assert any(item["lessonId"] == "01-01" for item in backup_payload["lessons"])

    fresh_client = _make_client(tmp_path / "fresh")
    import_resp = fresh_client.post("/api/progress/import", json=backup_payload)
    assert import_resp.status_code == 200
    restored = fresh_client.get("/api/lessons/01-01").json()
    assert restored["progress"]["notes"] == "Backup note check"
    assert restored["progress"]["status"] == "COMPLETED"

    # Reset clears hints_revealed and solution_revealed for a cold retry
    reset_resp = client.post("/api/lessons/01-01/reset")
    assert reset_resp.status_code == 200
    after_reset = client.get("/api/lessons/01-01").json()["progress"]
    assert after_reset["solutionRevealed"] is False
    assert after_reset["hintsRevealed"] == 0


def test_demo_mode_blocks_arbitrary_code_execution_and_import(tmp_path: Path) -> None:
    settings = Settings(
        db_path=tmp_path / "demo.db",
        curriculum_dir=REPO_ROOT / "curriculum",
        web_dist_dir=tmp_path / "missing_dist",
        demo_mode=True,
    )
    client = TestClient(create_app(settings))
    assert client.get("/api/health").json()["demoMode"] is True

    run_resp = client.post(
        "/api/lessons/01-01/run",
        json={"files": {"config_parser.py": "print('arbitrary')\n"}},
    )
    assert run_resp.status_code == 403

    import_resp = client.post("/api/progress/import", json={"version": "1.0"})
    assert import_resp.status_code == 403
