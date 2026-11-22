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

    port = int(raw_port.strip())
    timeout_sec = float(raw_timeout.strip())
    tls_enabled = raw_tls.strip().lower() in _TRUTHY

    return {
        "service_name": cleaned_name,
        "port": port,
        "timeout_sec": timeout_sec,
        "tls_enabled": tls_enabled,
        "region": region,
    }
