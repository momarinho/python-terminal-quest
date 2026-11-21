from __future__ import annotations

import hashlib
import hmac
import json
import time
from collections.abc import Callable


class WebhookSecurityError(PermissionError):
    """Raised when a webhook timestamp or HMAC-SHA256 signature is invalid or expired."""


def sign_payload(secret: bytes, timestamp: int, raw_body: bytes) -> str:
    """Return 'sha256=<hex>' HMAC signature over '{timestamp}.{raw_body}'."""
    msg = f"{timestamp}.".encode() + raw_body
    digest = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


class WebhookSignatureVerifier:
    def __init__(
        self,
        secret: bytes,
        max_age_seconds: int = 300,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._secret = secret
        self._max_age_seconds = max_age_seconds
        self._clock = clock

    def verify_and_parse(
        self,
        timestamp_header: str,
        signature_header: str,
        raw_body: bytes,
    ) -> dict[str, object]:
        """Verify replay window + constant-time HMAC-SHA256 and parse JSON object."""
        try:
            ts = int(timestamp_header.strip())
        except (TypeError, ValueError) as exc:
            raise WebhookSecurityError("Invalid webhook timestamp header") from exc

        if abs(self._clock() - ts) > self._max_age_seconds:
            raise WebhookSecurityError("Webhook timestamp outside allowed replay window")

        expected = sign_payload(self._secret, ts, raw_body)
        if not hmac.compare_digest(expected, signature_header.strip()):
            raise WebhookSecurityError("Webhook HMAC signature mismatch")

        try:
            parsed = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WebhookSecurityError("Webhook payload is not valid UTF-8 JSON") from exc

        if not isinstance(parsed, dict):
            raise WebhookSecurityError("Webhook payload must decode to a JSON object")
        return {str(k): v for k, v in parsed.items()}
