from regex_extractor import mask_bearer_tokens, parse_access_entry


def test_parse_access_entry_with_named_groups() -> None:
    parsed = parse_access_entry("  POST /v1/orders -> 201 (38ms) ")
    assert parsed == {
        "method": "POST",
        "path": "/v1/orders",
        "status": 201,
        "latency_ms": 38,
    }
    assert parse_access_entry("INVALID LOG LINE") is None


def test_mask_bearer_tokens_preserves_surrounding_text() -> None:
    raw = "Authorization: Bearer eyJhbGci.payload.sig user=ana"
    assert mask_bearer_tokens(raw) == "Authorization: Bearer [REDACTED] user=ana"
    assert mask_bearer_tokens("bearer secret123") == "bearer [REDACTED]"
