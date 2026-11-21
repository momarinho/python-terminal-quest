## Boss Fight: Inventory Reservation Engine

E-commerce checkouts reserve multiple SKUs atomically: if SKU A has 5 units in stock and SKU B has 0, reserving `[("A", 2), ("B", 1)]` must fail **and roll back SKU A** so inventory never drifts or oversells.

### Multi-File Architecture (`schema.py` + `engine.py`)
1. **`schema.py` -> `init_schema(conn: sqlite3.Connection) -> None`**
   * Create `skus (sku TEXT PRIMARY KEY, stock INTEGER NOT NULL CHECK(stock >= 0), version INTEGER NOT NULL DEFAULT 1)`.
   * Create `reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, res_id TEXT NOT NULL, sku TEXT NOT NULL, qty INTEGER NOT NULL CHECK(qty > 0), status TEXT NOT NULL)` with composite index `idx_res_lookup ON reservations (res_id, sku)`.
2. **`engine.py` -> Exceptions & Operations**
   * `ReservationError(Exception)` and `StockConflictError(ReservationError)`.
   * `seed_sku(conn, sku, stock)` (idempotent or insert) & `get_sku(conn, sku) -> dict[str, int | str] | None`.
   * `reserve_order(conn, res_id: str, items: list[tuple[str, int]]) -> list[dict[str, object]]`:
     * Reject blank `res_id`, empty `items`, or `qty <= 0` with `ReservationError`.
     * Inside **one** `BEGIN IMMEDIATE` transaction:
       * For each `(sku, qty)`: read current `(stock, version)` (raise `ReservationError` if unknown SKU), verify `stock >= qty` (else raise `StockConflictError`), and execute `UPDATE skus SET stock = stock - ?, version = version + 1 WHERE sku = ? AND version = ? AND stock >= ?` (checking `cur.rowcount == 1`).
       * Insert a row into `reservations (res_id, sku, qty, status)` with `status = "RESERVED"`.
       * On **any** failure mid-order, `conn.rollback()` so zero partial SKUs are decremented!
       * `conn.commit()` on full success and return reserved items.
