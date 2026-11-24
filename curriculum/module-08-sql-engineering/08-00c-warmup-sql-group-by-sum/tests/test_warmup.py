import sqlite3

from warmup import sum_qty_by_warehouse


def _seed_stock() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE stock (warehouse TEXT NOT NULL, qty INTEGER NOT NULL)")
    conn.executemany(
        "INSERT INTO stock (warehouse, qty) VALUES (?, ?)",
        [("east", 5), ("west", 12), ("east", 7)],
    )
    return conn


def test_sum_qty_by_warehouse() -> None:
    assert sum_qty_by_warehouse(_seed_stock()) == {"east": 12, "west": 12}


def test_sum_qty_empty_table() -> None:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE stock (warehouse TEXT NOT NULL, qty INTEGER NOT NULL)")
    assert sum_qty_by_warehouse(conn) == {}
