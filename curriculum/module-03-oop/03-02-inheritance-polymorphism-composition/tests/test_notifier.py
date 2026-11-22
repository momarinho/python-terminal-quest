import pytest
from notifier import (
    AlertDispatcher,
    EmailChannel,
    NotificationChannel,
    SlackChannel,
    WebhookChannel,
)


def test_polymorphic_channels_and_severity_filtering() -> None:
    email = EmailChannel("oncall-mail", "oncall@acme.dev", min_severity="warn")
    slack = SlackChannel("ops-slack", "#incidents", min_severity="info")
    hook = WebhookChannel("pager-hook", "https://hooks.internal/pager", min_severity="critical")
    assert isinstance(email, NotificationChannel)
    assert isinstance(slack, NotificationChannel)
    assert isinstance(hook, NotificationChannel)

    dispatcher = AlertDispatcher([slack])
    dispatcher.add_channel(email)
    dispatcher.add_channel(hook)

    assert dispatcher.dispatch("info", "Deploy started") == [
        "#incidents [INFO] Deploy started",
    ]
    assert dispatcher.dispatch("warn", "High CPU") == [
        "#incidents [WARN] High CPU",
        "[WARN] to=oncall@acme.dev :: High CPU",
    ]
    assert dispatcher.dispatch("critical", "DB down") == [
        "#incidents [CRITICAL] DB down",
        "[CRITICAL] to=oncall@acme.dev :: DB down",
        "POST https://hooks.internal/pager [CRITICAL] DB down",
    ]


def test_dispatch_by_channel_and_unknown_severity() -> None:
    dispatcher = AlertDispatcher(
        [
            SlackChannel("ops-slack", "ops", min_severity="info"),
            WebhookChannel("pager-hook", "https://hooks.internal/pager", min_severity="critical"),
        ]
    )
    assert dispatcher.dispatch_by_channel("warn", "Queue depth") == {
        "ops-slack": "#ops [WARN] Queue depth",
    }
    assert dispatcher.dispatch_by_channel("critical", "Outage") == {
        "ops-slack": "#ops [CRITICAL] Outage",
        "pager-hook": "POST https://hooks.internal/pager [CRITICAL] Outage",
    }
    with pytest.raises(ValueError):
        dispatcher.dispatch("debug", "noise")
    with pytest.raises(ValueError):
        dispatcher.dispatch_by_channel("debug", "noise")
