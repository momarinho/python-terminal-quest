_SEVERITY_RANK = {"info": 1, "warn": 2, "critical": 3}


class NotificationChannel:
    def __init__(self, name: str, min_severity: str = "info") -> None:
        self.name = name
        self.min_severity = min_severity.lower()

    def supports(self, severity: str) -> bool:
        """Return True iff `severity` meets or exceeds this channel's `min_severity`."""
        return _SEVERITY_RANK.get(severity.lower(), 0) >= _SEVERITY_RANK.get(self.min_severity, 1)

    def format_payload(self, severity: str, message: str) -> str:
        raise NotImplementedError


class EmailChannel(NotificationChannel):
    def __init__(self, name: str, recipient: str, min_severity: str = "warn") -> None:
        super().__init__(name, min_severity=min_severity)
        self.recipient = recipient

    def format_payload(self, severity: str, message: str) -> str:
        """Format '[SEVERITY] to=<recipient> :: <message>'."""
        return f"[{severity.upper()}] to={self.recipient} :: {message}"


class SlackChannel(NotificationChannel):
    def __init__(self, name: str, channel: str, min_severity: str = "info") -> None:
        super().__init__(name, min_severity=min_severity)
        self.channel = channel.lstrip("#")

    def format_payload(self, severity: str, message: str) -> str:
        """Format '#<channel> [SEVERITY] <message>'."""
        return f"#{self.channel} [{severity.upper()}] {message}"


class WebhookChannel(NotificationChannel):
    def __init__(self, name: str, endpoint: str, min_severity: str = "critical") -> None:
        super().__init__(name, min_severity=min_severity)
        self.endpoint = endpoint.strip()

    def format_payload(self, severity: str, message: str) -> str:
        """Format 'POST <endpoint> [SEVERITY] <message>'."""
        return f"POST {self.endpoint} [{severity.upper()}] {message}"


class AlertDispatcher:
    """Composes multiple NotificationChannel objects rather than inheriting from them."""

    def __init__(self, channels: list[NotificationChannel] | None = None) -> None:
        self.channels: list[NotificationChannel] = list(channels) if channels else []

    def add_channel(self, channel: NotificationChannel) -> None:
        self.channels.append(channel)

    def dispatch(self, severity: str, message: str) -> list[str]:
        """Validate severity and return formatted payloads for all supporting channels."""
        if severity.lower() not in _SEVERITY_RANK:
            raise ValueError(f"Unknown severity: {severity!r}")
        return [
            channel.format_payload(severity, message)
            for channel in self.channels
            if channel.supports(severity)
        ]

    def dispatch_by_channel(self, severity: str, message: str) -> dict[str, str]:
        """Validate severity and return {channel.name: formatted_payload} for supporting channels."""
        if severity.lower() not in _SEVERITY_RANK:
            raise ValueError(f"Unknown severity: {severity!r}")
        return {
            channel.name: channel.format_payload(severity, message)
            for channel in self.channels
            if channel.supports(severity)
        }
