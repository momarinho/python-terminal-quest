def route_event(event: dict[str, object]) -> str:
    """Route a webhook event dict to a dispatch action."""
    # TODO: implement structural match/case rules:
    # 1. {"type": "http", "status": int(s), "critical": True, "retries": int(r)} with 500 <= s < 600 and r < 3 -> "P1_RETRY"
    # 2. {"type": "http", "status": int(s)} with 500 <= s < 600 -> "P1_PAGE"
    # 3. {"type": "http", "status": 429} -> "RATE_LIMIT"
    # 4. {"type": "billing", "amount_cents": int(a)} with a > 0 -> "LEDGER_POST"
    # 5. {"type": "heartbeat"} -> "OK"
    # 6. fallback -> "IGNORE"
    return "IGNORE"
