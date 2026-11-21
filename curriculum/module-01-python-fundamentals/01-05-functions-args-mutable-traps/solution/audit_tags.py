def append_audit_tag(event: str, tags: list[str] | None = None) -> list[str]:
    """Append event to tags without leaking state across calls or mutating caller list."""
    result = list(tags) if tags is not None else []
    result.append(event)
    return result


def build_metric_event(
    metric: str,
    *labels: str,
    severity: str = "info",
    **attrs: str,
) -> dict[str, object]:
    """Build a structured metric dict with variadic labels, keyword-only severity, and attrs."""
    return {
        "metric": metric,
        "labels": list(labels),
        "severity": severity,
        "attrs": dict(attrs),
    }
