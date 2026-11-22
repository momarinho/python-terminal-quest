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
        # Add the remaining 3 cases before the fallback:
        # - {"type": "http", "status": 429} -> "RATE_LIMIT"
        # - {"type": "billing", "amount_cents": int(amount)} with amount > 0 -> "LEDGER_POST"
        # - {"type": "heartbeat"} -> "OK"
        case _:
            return "IGNORE"
