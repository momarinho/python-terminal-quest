_REQUIRED_KEYS = {"ts", "service", "status", "latency_ms"}


def parse_log_line(line: str) -> tuple[int, str, int, int]:
    """Parse 'ts=<int> service=<str> status=<int> latency_ms=<int>' into (ts, service, status, latency_ms)."""
    fields: dict[str, str] = {}
    for token in line.strip().split():
        if "=" not in token:
            raise ValueError(f"Malformed token: {token!r}")
        key, val = token.split("=", 1)
        fields[key.strip()] = val.strip()

    missing = _REQUIRED_KEYS - fields.keys()
    if missing:
        raise ValueError(f"Missing required log fields: {sorted(missing)}")

    ts = int(fields["ts"])
    service = fields["service"]
    status = int(fields["status"])
    latency_ms = int(fields["latency_ms"])

    if not service or ts < 0 or latency_ms < 0:
        raise ValueError("Invalid service, timestamp, or latency value")

    return ts, service, status, latency_ms
