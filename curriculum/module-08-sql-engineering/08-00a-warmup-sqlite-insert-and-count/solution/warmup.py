import sqlite3


def insert_item(conn: sqlite3.Connection, sku: str, qty: int) -> None:
    """Insert (sku, qty) into `items` using bind parameters."""
    conn.execute("INSERT INTO items (sku, qty) VALUES (?, ?)", (sku, qty))


def count_items(conn: sqlite3.Connection) -> int:
    """Return total rows in `items`."""
    row = conn.execute("SELECT COUNT(*) FROM items").fetchone()
    return int(row[0]) if row else 0
