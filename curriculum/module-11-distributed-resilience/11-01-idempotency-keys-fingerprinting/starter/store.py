from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    payload_hash: str
    status_code: int
    transaction_id: str
    debited_cents: int


def compute_payload_sha256(account_id: str, amount_cents: int, currency: str) -> str:
    """Return a deterministic SHA-256 hex digest of the canonical command payload."""
    # TODO: Use json.dumps with sort_keys=True, separators=(",", ":") and hashlib.sha256
    raise NotImplementedError("TODO: compute canonical SHA-256 fingerprint")


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[str, IdempotencyRecord] = {}

    def get(self, key: str) -> IdempotencyRecord | None:
        return self._records.get(key)

    def save(self, record: IdempotencyRecord) -> None:
        self._records[record.key] = record
