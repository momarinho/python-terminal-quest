from __future__ import annotations

import hashlib
import hmac
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
        # TODO:
        # 1. Parse timestamp_header to int (else WebhookSecurityError)
        # 2. Enforce abs(self._clock() - ts) <= self._max_age_seconds (else WebhookSecurityError)
        # 3. Compute sign_payload(...) and compare via hmac.compare_digest
        # 4. Return parsed dict from json.loads(raw_body)
        raise NotImplementedError("TODO: verify_and_parse")
