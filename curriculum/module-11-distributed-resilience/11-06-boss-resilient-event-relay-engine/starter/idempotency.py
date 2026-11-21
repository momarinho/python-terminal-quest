from __future__ import annotations


class IdempotencyConflictError(Exception):
    """Raised when an idempotency key is reused with a different payload fingerprint."""


def fingerprint_command(event_type: str, payload: dict[str, object]) -> str:
    """Return canonical SHA-256 hex digest for (event_type, payload)."""
    # TODO: Implement canonical SHA-256 digest
    raise NotImplementedError("TODO: fingerprint_command")
