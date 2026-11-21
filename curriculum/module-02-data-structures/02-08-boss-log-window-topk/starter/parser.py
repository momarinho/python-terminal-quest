def parse_log_line(line: str) -> tuple[int, str, int, int]:
    """Parse 'ts=<int> service=<str> status=<int> latency_ms=<int>' into (ts, service, status, latency_ms)."""
    # TODO: parse key=value tokens in any order and validate types/bounds
    raise ValueError("Not implemented")
