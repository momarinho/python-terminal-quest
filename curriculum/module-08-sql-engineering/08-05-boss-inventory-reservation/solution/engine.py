import sqlite3


class ReservationError(Exception):
    """Base error for inventory reservation failures."""


class StockConflictError(ReservationError):
    """Raised when stock is insufficient or optimistic version check fails."""


def seed_sku(conn: sqlite3.Connection, sku: str, stock: int) -> None:
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            "INSERT INTO skus (sku, stock, version) VALUES (?, ?, 1)",
            (sku, stock),
        )
        conn.commit()
    except BaseException:
        conn.rollback()
        raise


def get_sku(conn: sqlite3.Connection, sku: str) -> dict[str, int | str] | None:
    row = conn.execute(
        "SELECT sku, stock, version FROM skus WHERE sku = ?",
        (sku,),
    ).fetchone()
    if row is None:
        return None
    return {"sku": str(row[0]), "stock": int(row[1]), "version": int(row[2])}


def reserve_order(
    conn: sqlite3.Connection,
    res_id: str,
    items: list[tuple[str, int]],
) -> list[dict[str, object]]:
    """Atomically reserve all (sku, qty) items under BEGIN IMMEDIATE with optimistic lock."""
    cleaned_id = res_id.strip()
    if not cleaned_id or not items:
        raise ReservationError("Reservation requires non-blank res_id and at least one item")
    if any(qty <= 0 or not sku.strip() for sku, qty in items):
        raise ReservationError("Each item requires non-blank sku and positive qty")

    conn.execute("BEGIN IMMEDIATE")
    try:
        reserved: list[dict[str, object]] = []
        for raw_sku, qty in items:
            sku = raw_sku.strip()
            row = conn.execute(
                "SELECT stock, version FROM skus WHERE sku = ?",
                (sku,),
            ).fetchone()
            if row is None:
                raise ReservationError(f"Unknown SKU: {sku}")
            stock, version = int(row[0]), int(row[1])
            if stock < qty:
                raise StockConflictError(f"Insufficient stock for {sku}: need {qty}, have {stock}")

            cur = conn.execute(
                """
                UPDATE skus
                SET stock = stock - ?, version = version + 1
                WHERE sku = ? AND version = ? AND stock >= ?
                """,
                (qty, sku, version, qty),
            )
            if cur.rowcount != 1:
                raise StockConflictError(f"Optimistic lock conflict for SKU {sku}")

            conn.execute(
                "INSERT INTO reservations (res_id, sku, qty, status) VALUES (?, ?, ?, 'RESERVED')",
                (cleaned_id, sku, qty),
            )
            reserved.append({"res_id": cleaned_id, "sku": sku, "qty": qty, "status": "RESERVED"})

        conn.commit()
        return reserved
    except BaseException:
        conn.rollback()
        raise
