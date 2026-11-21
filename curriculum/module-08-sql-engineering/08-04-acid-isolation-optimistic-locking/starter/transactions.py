import sqlite3


class InsufficientFundsError(Exception):
    """Raised when source account lacks funds for atomic transfer."""


class OptimisticConflictError(Exception):
    """Raised when expected row version does not match current database version."""


def transfer_balance_atomic(
    conn: sqlite3.Connection,
    from_id: int,
    to_id: int,
    amount_cents: int,
) -> None:
    """Atomically move `amount_cents` from `from_id` to `to_id`, rolling back completely on error."""
    # TODO: BEGIN IMMEDIATE, debit source (check balance), credit target (check exists), COMMIT or ROLLBACK
    _ = (conn, from_id, to_id, amount_cents)


def update_tier_optimistic(
    conn: sqlite3.Connection,
    account_id: int,
    new_tier: str,
    expected_version: int,
) -> int:
    """Update account tier iff version == expected_version; return new version or raise OptimisticConflictError."""
    # TODO: UPDATE ... SET tier = ?, version = version + 1 WHERE id = ? AND version = ?, check rowcount
    return expected_version
