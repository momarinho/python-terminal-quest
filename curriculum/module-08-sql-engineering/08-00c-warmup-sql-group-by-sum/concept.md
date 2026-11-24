## Beginner Warm-Up 3: `GROUP BY` & `SUM()`

Let the SQL database summarize rows instead of pulling every row into Python:

```python
def sum_qty_by_warehouse(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        "SELECT warehouse, SUM(qty) FROM stock GROUP BY warehouse ORDER BY warehouse"
    ).fetchall()
    return {str(row[0]): int(row[1]) for row in rows}
```

### Challenge
Implement `sum_qty_by_warehouse` in `warmup.py`.
