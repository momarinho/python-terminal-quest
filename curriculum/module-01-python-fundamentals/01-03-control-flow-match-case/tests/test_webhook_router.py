from webhook_router import route_event


def test_http_5xx_zero_retries_is_not_treated_as_missing() -> None:
    assert (
        route_event({"type": "http", "status": 503, "critical": True, "retries": 0})
        == "P1_RETRY"
    )
    assert (
        route_event({"type": "http", "status": 502, "critical": True, "retries": 2})
        == "P1_RETRY"
    )
    assert (
        route_event({"type": "http", "status": 500, "critical": True, "retries": 3})
        == "P1_PAGE"
    )
    assert route_event({"type": "http", "status": 500, "critical": False}) == "P1_PAGE"


def test_rate_limit_billing_heartbeat_and_fallback() -> None:
    assert route_event({"type": "http", "status": 429}) == "RATE_LIMIT"
    assert route_event({"type": "billing", "amount_cents": 1500}) == "LEDGER_POST"
    assert route_event({"type": "billing", "amount_cents": 0}) == "IGNORE"
    assert route_event({"type": "heartbeat", "extra": "ok"}) == "OK"
    assert route_event({"type": "unknown"}) == "IGNORE"
