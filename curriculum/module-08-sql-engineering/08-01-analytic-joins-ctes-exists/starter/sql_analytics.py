import sqlite3


def high_value_customers(
    conn: sqlite3.Connection,
    min_total_cents: int,
) -> list[dict[str, int | str]]:
    """Return [{'customer_id', 'name', 'total_cents', 'order_count'}] for non-cancelled totals >= min_total_cents."""
    # TODO: parameterized CTE + JOIN + GROUP BY + HAVING ordered by total_cents DESC, customer_id ASC
    _ = (conn, min_total_cents)
    return []


def customers_without_refunds(conn: sqlite3.Connection) -> list[int]:
    """Return sorted customer IDs that have zero rows in `refunds` (must be NULL-safe)."""
    # TODO: use NOT EXISTS (not NOT IN!)
    return []
