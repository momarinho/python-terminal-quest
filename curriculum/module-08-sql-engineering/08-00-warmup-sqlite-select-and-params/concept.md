## Concept: Warm-Up & Quick Syntax Reveal (Module 8)

Rule #1 of SQL engineering: **never concatenate user strings into SQL queries**. Always bind parameters with `?` tuples!

### Pattern Reveal #1 — Parameterized `INSERT`
```python
def insert_item(conn: sqlite3.Connection, sku: str, qty: int) -> None:
    conn.execute("INSERT INTO items (sku, qty) VALUES (?, ?)", (sku, qty))
```

### Pattern Reveal #2 — Parameterized `SELECT ... ORDER BY`
```python
def fetch_in_stock_skus(conn: sqlite3.Connection, min_qty: int) -> list[str]:
    rows = conn.execute(
        "SELECT sku FROM items WHERE qty >= ? ORDER BY sku",
        (min_qty,),
    ).fetchall()
    return [row[0] for row in rows]
```

### Pattern Reveal #3 — Aggregate `COUNT(*)` via `fetchone()`
```python
def count_items(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM items").fetchone()
    return int(row[0]) if row else 0
```

### Challenge
Open `warmup.py` and complete all 3 parameterized SQL helpers (table `items(sku TEXT, qty INTEGER)` is already created in tests).
