import sqlite3


def sum_qty_by_warehouse(conn: sqlite3.Connection) -> dict[str, int]:
    """Return total qty per warehouse from the `stock` table."""
    rows = conn.execute(
        "SELECT warehouse, SUM(qty) FROM stock GROUP BY warehouse ORDER BY warehouse"
    ).fetchall()
    return {str(row[0]): int(row[1]) for row in rows}
