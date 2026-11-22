_SEVERITY_RANK = {"info": 1, "warn": 2, "critical": 3}


class NotificationChannel:
    def __init__(self, name: str, min_severity: str = "info") -> None:
        self.name = name
        self.min_severity = min_severity.lower()

    def supports(self, severity: str) -> bool:
        """Return True iff `severity` meets or exceeds this channel's `min_severity`."""
        return False

    def format_payload(self, severity: str, message: str) -> str:
        raise NotImplementedError


class EmailChannel(NotificationChannel):
    def __init__(self, name: str, recipient: str, min_severity: str = "warn") -> None:
        super().__init__(name, min_severity=min_severity)
        self.recipient = recipient

    def format_payload(self, severity: str, message: str) -> str:
        """Format '[SEVERITY] to=<recipient> :: <message>'."""
        return ""


class SlackChannel(NotificationChannel):
    def __init__(self, name: str, channel: str, min_severity: str = "info") -> None:
        super().__init__(name, min_severity=min_severity)
        self.channel = channel.lstrip("#")

    def format_payload(self, severity: str, message: str) -> str:
        """Format '#<channel> [SEVERITY] <message>'."""
        return ""


class WebhookChannel(NotificationChannel):
    def __init__(self, name: str, endpoint: str, min_severity: str = "critical") -> None:
        super().__init__(name, min_severity=min_severity)
        self.endpoint = endpoint.strip()

    def format_payload(self, severity: str, message: str) -> str:
        """Format 'POST <endpoint> [SEVERITY] <message>'."""
        return ""


class AlertDispatcher:
    """Composes multiple NotificationChannel objects rather than inheriting from them."""

    def __init__(self, channels: list[NotificationChannel] | None = None) -> None:
        self.channels: list[NotificationChannel] = list(channels) if channels else []

    def add_channel(self, channel: NotificationChannel) -> None:
        self.channels.append(channel)

    def dispatch(self, severity: str, message: str) -> list[str]:
        """Validate severity and return formatted payloads for all supporting channels."""
        return []

    def dispatch_by_channel(self, severity: str, message: str) -> dict[str, str]:
        """Validate severity and return {channel.name: formatted_payload} for supporting channels."""
        return {}
