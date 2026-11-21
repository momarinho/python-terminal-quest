_SEVERITY_RANK = {"info": 1, "warn": 2, "critical": 3}


class NotificationChannel:
    def __init__(self, name: str, min_severity: str = "info") -> None:
        self.name = name
        self.min_severity = min_severity.lower()

    def supports(self, severity: str) -> bool:
        return _SEVERITY_RANK.get(severity.lower(), 0) >= _SEVERITY_RANK.get(self.min_severity, 1)

    def format_payload(self, severity: str, message: str) -> str:
        raise NotImplementedError


class EmailChannel(NotificationChannel):
    def __init__(self, name: str, recipient: str, min_severity: str = "warn") -> None:
        super().__init__(name, min_severity=min_severity)
        self.recipient = recipient

    def format_payload(self, severity: str, message: str) -> str:
        # TODO: return '[SEVERITY] to=<recipient> :: <message>'
        return ""


class SlackChannel(NotificationChannel):
    def __init__(self, name: str, channel: str, min_severity: str = "info") -> None:
        super().__init__(name, min_severity=min_severity)
        self.channel = channel.lstrip("#")

    def format_payload(self, severity: str, message: str) -> str:
        # TODO: return '#<channel> [SEVERITY] <message>'
        return ""


class AlertDispatcher:
    """Composes multiple NotificationChannel objects rather than inheriting from them."""

    def __init__(self, channels: list[NotificationChannel] | None = None) -> None:
        self.channels: list[NotificationChannel] = list(channels) if channels else []

    def add_channel(self, channel: NotificationChannel) -> None:
        self.channels.append(channel)

    def dispatch(self, severity: str, message: str) -> list[str]:
        # TODO: collect format_payload() outputs for all channels supporting `severity`
        return []
