_TRUTHY = {"1", "true", "yes", "on"}


def parse_service_config(
    service_name: str,
    raw_port: str,
    raw_timeout: str,
    raw_tls: str,
    raw_region: str | None = None,
) -> dict[str, int | float | bool | str | None]:
    """Parse raw environment strings into typed service configuration."""
    cleaned_name = service_name.strip()
    region = (raw_region.strip() or None) if raw_region is not None else None

    # Cast raw_port to int, raw_timeout to float, and check raw_tls against _TRUTHY
    port = 0
    timeout_sec = 0.0
    tls_enabled = bool(raw_tls)

    return {
        "service_name": cleaned_name,
        "port": port,
        "timeout_sec": timeout_sec,
        "tls_enabled": tls_enabled,
        "region": region,
    }
