import sqlite3

from warmup import count_items, insert_item


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (sku TEXT NOT NULL, qty INTEGER NOT NULL)")
    return conn


def test_insert_and_count_empty() -> None:
    conn = _db()
    assert count_items(conn) == 0
    insert_item(conn, "SKU-1", 10)
    insert_item(conn, "SKU-2", 4)
    assert count_items(conn) == 2


def test_insert_with_quotes_safely_bound() -> None:
    conn = _db()
    insert_item(conn, "SKU-'SAFE'", 1)
    assert count_items(conn) == 1
