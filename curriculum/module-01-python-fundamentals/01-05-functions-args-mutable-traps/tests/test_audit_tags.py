from audit_tags import append_audit_tag, build_metric_event


def test_append_audit_tag_has_no_mutable_default_leak() -> None:
    first = append_audit_tag("login")
    second = append_audit_tag("logout")
    assert first == ["login"]
    assert second == ["logout"]

    existing = ["init"]
    updated = append_audit_tag("ready", existing)
    assert updated == ["init", "ready"]
    assert existing == ["init"]


def test_build_metric_event_args_kwonly_and_kwargs() -> None:
    event = build_metric_event(
        "http_errors",
        "checkout",
        "eu-west",
        severity="critical",
        status="503",
        pod="web-7",
    )
    assert event == {
        "metric": "http_errors",
        "labels": ["checkout", "eu-west"],
        "severity": "critical",
        "attrs": {"status": "503", "pod": "web-7"},
    }
