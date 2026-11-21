import sqlite3

import pytest
from engine import StockConflictError, get_sku, reserve_order, seed_sku
from schema import init_schema


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", isolation_level=None)
    init_schema(conn)
    seed_sku(conn, "SKU-A", 5)
    seed_sku(conn, "SKU-B", 1)
    return conn


def test_atomic_multi_sku_reservation_succeeds_and_bumps_versions() -> None:
    conn = _db()
    reserved = reserve_order(conn, "ORD-1", [("SKU-A", 2), ("SKU-B", 1)])
    assert len(reserved) == 2
    assert get_sku(conn, "SKU-A") == {"sku": "SKU-A", "stock": 3, "version": 2}
    assert get_sku(conn, "SKU-B") == {"sku": "SKU-B", "stock": 0, "version": 2}

    plan = conn.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM reservations WHERE res_id = ? AND sku = ?",
        ("ORD-1", "SKU-A"),
    ).fetchall()
    assert any("USING INDEX" in str(row[3]).upper() for row in plan)


def test_partial_failure_rolls_back_all_skus_preventing_oversell() -> None:
    conn = _db()
    with pytest.raises(StockConflictError):
        reserve_order(conn, "ORD-FAIL", [("SKU-A", 4), ("SKU-B", 2)])

    # SKU-A must be rolled back completely to 5 (version 1) and zero reservation rows persisted!
    assert get_sku(conn, "SKU-A") == {"sku": "SKU-A", "stock": 5, "version": 1}
    assert conn.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 0
