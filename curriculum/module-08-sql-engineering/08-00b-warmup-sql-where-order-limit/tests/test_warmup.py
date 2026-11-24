import sqlite3

from warmup import top_skus


def _seed() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (sku TEXT NOT NULL, qty INTEGER NOT NULL)")
    conn.executemany(
        "INSERT INTO items (sku, qty) VALUES (?, ?)",
        [("A", 2), ("B", 20), ("C", 15), ("D", 20)],
    )
    return conn


def test_top_skus_filters_orders_and_limits() -> None:
    conn = _seed()
    assert top_skus(conn, 10, 2) == ["B", "D"]


def test_top_skus_returns_all_matching_within_limit() -> None:
    conn = _seed()
    assert top_skus(conn, 15, 5) == ["B", "D", "C"]
