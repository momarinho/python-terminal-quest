import sqlite3


def init_schema(conn: sqlite3.Connection) -> None:
    """Create `skus`, `reservations`, and `idx_res_lookup` composite index."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS skus (
            sku TEXT PRIMARY KEY,
            stock INTEGER NOT NULL CHECK (stock >= 0),
            version INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            res_id TEXT NOT NULL,
            sku TEXT NOT NULL,
            qty INTEGER NOT NULL CHECK (qty > 0),
            status TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_res_lookup
        ON reservations (res_id, sku);
        """
    )
