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
    if amount_cents <= 0 or from_id == to_id:
        raise ValueError("Invalid transfer amount or identical accounts")

    conn.execute("BEGIN IMMEDIATE")
    try:
        src_row = conn.execute(
            "SELECT balance_cents FROM accounts WHERE id = ?",
            (from_id,),
        ).fetchone()
        if src_row is None:
            raise ValueError(f"Source account {from_id} not found")
        if int(src_row[0]) < amount_cents:
            raise InsufficientFundsError("Insufficient funds")

        conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents - ? WHERE id = ?",
            (amount_cents, from_id),
        )
        cur = conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents + ? WHERE id = ?",
            (amount_cents, to_id),
        )
        if cur.rowcount != 1:
            raise ValueError(f"Target account {to_id} not found")
        conn.commit()
    except BaseException:
        conn.rollback()
        raise


def update_tier_optimistic(
    conn: sqlite3.Connection,
    account_id: int,
    new_tier: str,
    expected_version: int,
) -> int:
    """Update account tier iff version == expected_version; return new version or raise OptimisticConflictError."""
    conn.execute("BEGIN IMMEDIATE")
    try:
        cur = conn.execute(
            """
            UPDATE accounts
            SET tier = ?, version = version + 1
            WHERE id = ? AND version = ?
            """,
            (new_tier, account_id, expected_version),
        )
        if cur.rowcount != 1:
            raise OptimisticConflictError(
                f"Version mismatch for account {account_id} (expected {expected_version})"
            )
        conn.commit()
        return expected_version + 1
    except BaseException:
        conn.rollback()
        raise
