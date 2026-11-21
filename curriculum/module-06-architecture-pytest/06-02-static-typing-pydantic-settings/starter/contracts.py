from typing import Protocol

from settings import AppSettings


class ClockProtocol(Protocol):
    def now_iso(self) -> str: ...


def build_audit_header(settings: AppSettings, clock: ClockProtocol) -> dict[str, str]:
    """Build outbound headers using ClockProtocol and SecretStr.get_secret_value()."""
    # TODO: return X-Service, X-Timestamp, and Authorization Bearer <secret>
    _ = (settings, clock)
    return {}
