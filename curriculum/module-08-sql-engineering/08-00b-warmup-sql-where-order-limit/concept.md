## Beginner Warm-Up 2: `WHERE`, `ORDER BY` & `LIMIT`

Writing clear `SELECT ... WHERE ... ORDER BY ... LIMIT` queries is the foundation for every analytics and pagination stage in Module 8:

```python
def top_skus(conn: sqlite3.Connection, min_qty: int, limit: int) -> list[str]:
    rows = conn.execute(
        "SELECT sku FROM items WHERE qty >= ? ORDER BY qty DESC, sku ASC LIMIT ?",
        (min_qty, limit),
    ).fetchall()
    return [str(r[0]) for r in rows]
```

### Challenge
Implement `top_skus` in `warmup.py`.
