import sqlite3


def insert_item(conn: sqlite3.Connection, sku: str, qty: int) -> None:
    """Insert a SKU and quantity into `items` using bind parameters."""
    # Reveal: conn.execute("INSERT INTO items (sku, qty) VALUES (?, ?)", (sku, qty))
    pass


def fetch_in_stock_skus(conn: sqlite3.Connection, min_qty: int) -> list[str]:
    """Return sorted SKUs from `items` where qty >= min_qty."""
    # Reveal: SELECT sku FROM items WHERE qty >= ? ORDER BY sku
    return []


def count_items(conn: sqlite3.Connection) -> int:
    """Return total row count in `items`."""
    # Reveal: row = conn.execute("SELECT COUNT(*) FROM items").fetchone()
    return -1
