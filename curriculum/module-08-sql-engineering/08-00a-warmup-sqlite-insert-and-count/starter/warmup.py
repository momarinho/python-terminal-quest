import sqlite3


def insert_item(conn: sqlite3.Connection, sku: str, qty: int) -> None:
    """Insert (sku, qty) into `items` using bind parameters."""
    pass


def count_items(conn: sqlite3.Connection) -> int:
    """Return total rows in `items`."""
    return -1
