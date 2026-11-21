import sqlite3


def init_schema(conn: sqlite3.Connection) -> None:
    """Create `skus`, `reservations`, and `idx_res_lookup` composite index."""
    # TODO: create skus and reservations tables + composite index (res_id, sku)
    _ = conn
