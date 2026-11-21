from typing import Protocol

from settings import AppSettings


class ClockProtocol(Protocol):
    def now_iso(self) -> str: ...


def build_audit_header(settings: AppSettings, clock: ClockProtocol) -> dict[str, str]:
    """Build outbound headers using ClockProtocol and SecretStr.get_secret_value()."""
    return {
        "X-Service": settings.service_name,
        "X-Timestamp": clock.now_iso(),
        "Authorization": f"Bearer {settings.api_token.get_secret_value()}",
    }
