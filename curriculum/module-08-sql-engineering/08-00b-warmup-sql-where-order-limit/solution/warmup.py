import sqlite3


def top_skus(conn: sqlite3.Connection, min_qty: int, limit: int) -> list[str]:
    """Return top `limit` SKUs with qty >= min_qty, ordered by qty DESC then sku ASC."""
    rows = conn.execute(
        "SELECT sku FROM items WHERE qty >= ? ORDER BY qty DESC, sku ASC LIMIT ?",
        (min_qty, limit),
    ).fetchall()
    return [str(r[0]) for r in rows]
