from __future__ import annotations

import hashlib
import json


class IdempotencyConflictError(Exception):
    """Raised when an idempotency key is reused with a different payload fingerprint."""


def fingerprint_command(event_type: str, payload: dict[str, object]) -> str:
    """Return canonical SHA-256 hex digest for (event_type, payload)."""
    canonical = json.dumps(
        {"event_type": event_type, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
