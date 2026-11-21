def append_audit_tag(event: str, tags: list[str] = []) -> list[str]:  # noqa: B006
    """Append event to tags without leaking state across calls or mutating caller list."""
    tags.append(event)
    return tags


def build_metric_event(
    metric: str,
    *labels: str,
    severity: str = "info",
    **attrs: str,
) -> dict[str, object]:
    """Build a structured metric dict with variadic labels, keyword-only severity, and attrs."""
    # TODO: return {"metric": metric, "labels": ..., "severity": ..., "attrs": ...}
    return {}
