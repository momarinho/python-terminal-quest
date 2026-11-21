def parse_service_config(
    service_name: str,
    raw_port: str,
    raw_timeout: str,
    raw_tls: str,
    raw_region: str | None = None,
) -> dict[str, int | float | bool | str | None]:
    """Parse raw environment strings into typed service configuration."""
    # TODO: strip & validate service_name, cast port (1..65535) and timeout (> 0),
    # explicitly parse raw_tls ('true'/'1'/'yes'/'on' vs 'false'/'0'/'no'/'off'),
    # and normalize optional raw_region to None if blank.
    return {
        "service_name": service_name,
        "port": 0,
        "timeout_sec": 0.0,
        "tls_enabled": bool(raw_tls),
        "region": raw_region,
    }
