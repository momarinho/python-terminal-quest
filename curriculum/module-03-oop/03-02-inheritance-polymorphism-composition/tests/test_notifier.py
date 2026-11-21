import pytest
from notifier import AlertDispatcher, EmailChannel, NotificationChannel, SlackChannel


def test_polymorphic_channels_and_severity_filtering() -> None:
    email = EmailChannel("oncall-mail", "oncall@acme.dev", min_severity="warn")
    slack = SlackChannel("ops-slack", "#incidents", min_severity="info")
    assert isinstance(email, NotificationChannel)
    assert isinstance(slack, NotificationChannel)

    dispatcher = AlertDispatcher([slack])
    dispatcher.add_channel(email)

    assert dispatcher.dispatch("info", "Deploy started") == [
        "#incidents [INFO] Deploy started",
    ]
    assert dispatcher.dispatch("critical", "DB down") == [
        "#incidents [CRITICAL] DB down",
        "[CRITICAL] to=oncall@acme.dev :: DB down",
    ]


def test_rejects_unknown_severity() -> None:
    dispatcher = AlertDispatcher([SlackChannel("ops", "ops")])
    with pytest.raises(ValueError):
        dispatcher.dispatch("debug", "noise")
