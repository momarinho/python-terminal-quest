def route_event(event: dict[str, object]) -> str:
    """Route a webhook event dict to a dispatch action."""
    match event:
        case {
            "type": "http",
            "status": int(status),
            "critical": True,
            "retries": int(retries),
        } if 500 <= status < 600 and 0 <= retries < 3:
            return "P1_RETRY"
        case {"type": "http", "status": int(status)} if 500 <= status < 600:
            return "P1_PAGE"
        case {"type": "http", "status": 429}:
            return "RATE_LIMIT"
        case {"type": "billing", "amount_cents": int(amount)} if amount > 0:
            return "LEDGER_POST"
        case {"type": "heartbeat"}:
            return "OK"
        case _:
            return "IGNORE"
