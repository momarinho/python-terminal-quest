import pytest
from prompt_guard import (
    ChatMessage,
    estimate_tokens,
    scrub_pii,
    trim_conversation_history,
)


def test_scrub_pii_redacts_sensitive_fields() -> None:
    raw = (
        "Contact ana@acme.io (CPF 123.456.789-00, SSN 123-45-6789) "
        "with Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc and key sk-liveSecretKey9988."
    )
    scrubbed = scrub_pii(raw)
    assert "ana@acme.io" not in scrubbed
    assert "123.456.789-00" not in scrubbed
    assert "123-45-6789" not in scrubbed
    assert "eyJhbGciOiJIUzI1NiJ9.abc" not in scrubbed
    assert "sk-liveSecretKey9988" not in scrubbed
    assert "[EMAIL_REDACTED]" in scrubbed
    assert "[GOV_ID_REDACTED]" in scrubbed
    assert "Bearer [TOKEN_REDACTED]" in scrubbed
    assert "[API_KEY_REDACTED]" in scrubbed


def test_trim_history_preserves_system_and_latest_turns() -> None:
    system = "Be concise."
    history = [
        ChatMessage(role="user", content="Old turn 1 with very long context padding here " * 3),
        ChatMessage(role="assistant", content="Old reply 1 " * 6),
        ChatMessage(role="user", content="Recent user alice@example.com"),
        ChatMessage(role="assistant", content="Recent ok"),
    ]
    trimmed = trim_conversation_history(system, history, "Next question?", max_tokens=26)

    assert trimmed[0].role == "system"
    assert trimmed[-1].role == "user"
    assert trimmed[-1].content == "Next question?"
    assert sum(estimate_tokens(m.content) for m in trimmed) <= 26
    assert any("Recent ok" in m.content for m in trimmed)
    assert all("alice@example.com" not in m.content for m in trimmed)


def test_raises_when_system_and_query_exceed_budget() -> None:
    with pytest.raises(ValueError):
        trim_conversation_history("System " * 20, [], "Query " * 20, max_tokens=10)
