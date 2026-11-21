_TRUTHY = {"1", "true", "yes", "on"}
_FALSY = {"0", "false", "no", "off"}


def parse_service_config(
    service_name: str,
    raw_port: str,
    raw_timeout: str,
    raw_tls: str,
    raw_region: str | None = None,
) -> dict[str, int | float | bool | str | None]:
    """Parse raw environment strings into typed service configuration."""
    cleaned_name = service_name.strip()
    if not cleaned_name:
        raise ValueError("service_name must not be blank")

    port = int(raw_port.strip())
    if not (1 <= port <= 65535):
        raise ValueError(f"port out of range: {port}")

    timeout_sec = float(raw_timeout.strip())
    if timeout_sec <= 0:
        raise ValueError(f"timeout_sec must be positive: {timeout_sec}")

    tls_norm = raw_tls.strip().lower()
    if tls_norm in _TRUTHY:
        tls_enabled = True
    elif tls_norm in _FALSY:
        tls_enabled = False
    else:
        raise ValueError(f"invalid boolean value for raw_tls: {raw_tls!r}")

    region: str | None = None
    if raw_region is not None:
        stripped_region = raw_region.strip()
        region = stripped_region or None

    return {
        "service_name": cleaned_name,
        "port": port,
        "timeout_sec": timeout_sec,
        "tls_enabled": tls_enabled,
        "region": region,
    }
