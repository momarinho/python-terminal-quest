from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from pyquest.api.app import create_app
from pyquest.config import Settings

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_DIR = REPO_ROOT / "curriculum"


def test_oracle_ask_returns_valid_diy_stub_response(tmp_path: Path) -> None:
    settings = Settings(
        db_path=tmp_path / "progress.db",
        curriculum_dir=CURRICULUM_DIR,
        web_dist_dir=tmp_path / "missing_dist",
    )
    client = TestClient(create_app(settings))
    resp = client.post(
        "/api/oracle/ask",
        json={
            "lessonId": "11-02",
            "question": "How does a Circuit Breaker transition from OPEN to HALF_OPEN?",
            "files": {"breaker.py": "class CircuitBreaker:\n    pass\n"},
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "stub"
    assert body["provider"] == "stub"
    assert body["guardrailTriggered"] is False
    assert isinstance(body["latencyMs"], int)
    assert body["citations"][0]["lessonId"] == "11-02"
    assert "CAPSTONE_README.md" in body["answer"]


@pytest.mark.skip(reason="DIY Capstone: unskip after implementing src/pyquest/rag/")
def test_capstone_indexer_never_indexes_solution_or_test_files() -> None:
    """Verify your indexer loads concept.md + lesson.yaml only and rejects solution/ and tests/."""
    raise AssertionError("Implement curriculum indexer in src/pyquest/rag/ and enable this check")


@pytest.mark.skip(reason="DIY Capstone: unskip after implementing src/pyquest/rag/")
def test_capstone_grounded_retrieval_returns_lesson_citations() -> None:
    """Verify hybrid retrieval returns relevant [lesson-id] citations (e.g. 09-02, 10-02, 01-09)."""
    raise AssertionError("Implement hybrid VectorStore retrieval and enable this check")


@pytest.mark.skip(reason="DIY Capstone: unskip after implementing src/pyquest/rag/")
def test_capstone_prompt_injection_triggers_guardrail() -> None:
    """Verify prompt-injection or full-solution queries set guardrailTriggered=True with empty citations."""
    raise AssertionError("Implement prompt-injection guardrails + PII scrubbing and enable this check")


@pytest.mark.skip(reason="DIY Capstone: unskip after implementing src/pyquest/rag/")
def test_capstone_live_llm_and_graceful_offline_fallback() -> None:
    """Verify upstream LlmClient failures fall back seamlessly to mode='offline-rag'."""
    raise AssertionError("Implement dual-mode Oracle fallback and enable this check")
