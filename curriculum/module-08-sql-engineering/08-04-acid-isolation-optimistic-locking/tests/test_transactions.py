import sqlite3

import pytest
from transactions import (
    InsufficientFundsError,
    OptimisticConflictError,
    transfer_balance_atomic,
    update_tier_optimistic,
)


def _seed_accounts() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.executescript(
        """
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY,
            balance_cents INTEGER NOT NULL,
            tier TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1
        );
        INSERT INTO accounts VALUES (1, 10000, 'starter', 1), (2, 2000, 'starter', 1);
        """
    )
    return conn


def test_transfer_rolls_back_atomically_if_target_missing() -> None:
    conn = _seed_accounts()
    transfer_balance_atomic(conn, 1, 2, 2500)
    assert conn.execute("SELECT balance_cents FROM accounts WHERE id = 1").fetchone()[0] == 7500
    assert conn.execute("SELECT balance_cents FROM accounts WHERE id = 2").fetchone()[0] == 4500

    with pytest.raises(ValueError):
        transfer_balance_atomic(conn, 1, 999, 1000)
    # Sender must remain untouched after rollback!
    assert conn.execute("SELECT balance_cents FROM accounts WHERE id = 1").fetchone()[0] == 7500

    with pytest.raises(InsufficientFundsError):
        transfer_balance_atomic(conn, 1, 2, 50_000)


def test_update_tier_optimistic_rejects_stale_version() -> None:
    conn = _seed_accounts()
    v2 = update_tier_optimistic(conn, 1, "growth", expected_version=1)
    assert v2 == 2
    with pytest.raises(OptimisticConflictError):
        update_tier_optimistic(conn, 1, "enterprise", expected_version=1)
