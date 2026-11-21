import sqlite3


def high_value_customers(
    conn: sqlite3.Connection,
    min_total_cents: int,
) -> list[dict[str, int | str]]:
    """Return [{'customer_id', 'name', 'total_cents', 'order_count'}] for non-cancelled totals >= min_total_cents."""
    sql = """
    WITH customer_totals AS (
        SELECT
            customer_id,
            SUM(amount_cents) AS total_cents,
            COUNT(*) AS order_count
        FROM orders
        WHERE status != 'CANCELLED'
        GROUP BY customer_id
        HAVING SUM(amount_cents) >= ?
    )
    SELECT
        c.id AS customer_id,
        c.name AS name,
        ct.total_cents AS total_cents,
        ct.order_count AS order_count
    FROM customers c
    JOIN customer_totals ct ON ct.customer_id = c.id
    ORDER BY ct.total_cents DESC, c.id ASC
    """
    rows = conn.execute(sql, (min_total_cents,)).fetchall()
    return [
        {
            "customer_id": int(r[0]),
            "name": str(r[1]),
            "total_cents": int(r[2]),
            "order_count": int(r[3]),
        }
        for r in rows
    ]


def customers_without_refunds(conn: sqlite3.Connection) -> list[int]:
    """Return sorted customer IDs that have zero rows in `refunds` (must be NULL-safe)."""
    sql = """
    SELECT c.id
    FROM customers c
    WHERE NOT EXISTS (
        SELECT 1 FROM refunds r WHERE r.customer_id = c.id
    )
    ORDER BY c.id ASC
    """
    return [int(row[0]) for row in conn.execute(sql).fetchall()]
