## Beginner Warm-Up 1: Parameterized `INSERT` & `COUNT(*)`

Always bind SQL values with `?` tuples rather than Python string formatting (`f"..."`):

```python
def insert_item(conn: sqlite3.Connection, sku: str, qty: int) -> None:
    conn.execute("INSERT INTO items (sku, qty) VALUES (?, ?)", (sku, qty))

def count_items(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM items").fetchone()
    return int(row[0]) if row else 0
```

### Challenge
Complete `insert_item` and `count_items` in `warmup.py`.
