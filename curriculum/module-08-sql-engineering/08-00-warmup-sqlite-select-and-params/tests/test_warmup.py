import sqlite3

from warmup import count_items, fetch_in_stock_skus, insert_item


def _make_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (sku TEXT NOT NULL, qty INTEGER NOT NULL)")
    return conn


def test_insert_and_count_items() -> None:
    conn = _make_conn()
    insert_item(conn, "SKU-B", 5)
    insert_item(conn, "SKU-A", 1)
    assert count_items(conn) == 2


def test_fetch_in_stock_skus_filters_and_sorts() -> None:
    conn = _make_conn()
    insert_item(conn, "SKU-C", 10)
    insert_item(conn, "SKU-A", 12)
    insert_item(conn, "SKU-B", 2)
    assert fetch_in_stock_skus(conn, 5) == ["SKU-A", "SKU-C"]
