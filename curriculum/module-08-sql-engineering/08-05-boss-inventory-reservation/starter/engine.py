import sqlite3


class ReservationError(Exception):
    """Base error for inventory reservation failures."""


class StockConflictError(ReservationError):
    """Raised when stock is insufficient or optimistic version check fails."""


def seed_sku(conn: sqlite3.Connection, sku: str, stock: int) -> None:
    # TODO: insert SKU with version=1
    _ = (conn, sku, stock)


def get_sku(conn: sqlite3.Connection, sku: str) -> dict[str, int | str] | None:
    # TODO: return {'sku': ..., 'stock': ..., 'version': ...} or None
    return None


def reserve_order(
    conn: sqlite3.Connection,
    res_id: str,
    items: list[tuple[str, int]],
) -> list[dict[str, object]]:
    """Atomically reserve all (sku, qty) items under BEGIN IMMEDIATE with optimistic lock."""
    # TODO: validate inputs, BEGIN IMMEDIATE, decrement each SKU with version check, insert reservations, COMMIT/ROLLBACK
    return []
