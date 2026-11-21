def is_release_ready(checks: list[dict[str, object]]) -> bool:
    """Return True iff checks is non-empty and every check has passed=True."""
    return bool(checks) and all(bool(item.get("passed")) for item in checks)


def has_blocking_alert(alerts: list[dict[str, object]]) -> bool:
    """Return True if any alert has severity == 'critical' and acked == False."""
    return any(
        alert.get("severity") == "critical" and not bool(alert.get("acked", False))
        for alert in alerts
    )


def rank_endpoints(endpoints: list[dict[str, object]]) -> list[str]:
    """Return endpoint paths ordered by highest error_rate, then highest p99_ms, then path asc."""
    ordered = sorted(
        endpoints,
        key=lambda ep: (
            -float(ep["error_rate"]),
            -int(ep["p99_ms"]),
            str(ep["path"]),
        ),
    )
    return [str(ep["path"]) for ep in ordered]


def fastest_healthy_region(regions: list[dict[str, object]]) -> str:
    """Return the name of the healthy region with lowest latency_ms (tie-break name asc)."""
    healthy = [region for region in regions if bool(region.get("healthy"))]
    if not healthy:
        raise ValueError("No healthy regions available")
    best = min(healthy, key=lambda r: (int(r["latency_ms"]), str(r["name"])))
    return str(best["name"])
