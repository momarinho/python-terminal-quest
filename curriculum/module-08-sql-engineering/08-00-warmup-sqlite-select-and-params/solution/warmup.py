import sqlite3


def insert_item(conn: sqlite3.Connection, sku: str, qty: int) -> None:
    """Insert a SKU and quantity into `items` using bind parameters."""
    conn.execute("INSERT INTO items (sku, qty) VALUES (?, ?)", (sku, qty))


def fetch_in_stock_skus(conn: sqlite3.Connection, min_qty: int) -> list[str]:
    """Return sorted SKUs from `items` where qty >= min_qty."""
    rows = conn.execute(
        "SELECT sku FROM items WHERE qty >= ? ORDER BY sku",
        (min_qty,),
    ).fetchall()
    return [str(row[0]) for row in rows]


def count_items(conn: sqlite3.Connection) -> int:
    """Return total row count in `items`."""
    row = conn.execute("SELECT COUNT(*) FROM items").fetchone()
    return int(row[0]) if row else 0
