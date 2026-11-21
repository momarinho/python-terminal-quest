## Concept: Keyset (Cursor) Pagination vs. `OFFSET` Drift

`LIMIT 20 OFFSET 10000` forces the database to scan and discard 10,000 rows—and if a new row is inserted while a user paginates, row 20 shifts into page 2 as a **duplicate**!

### Deterministic Keyset Cursor `(created_at DESC, id DESC)`
Filter directly past the last seen `(created_at, id)` pair using row-value comparison `(created_at, id) < (?, ?)` (or explicit `(created_at < ? OR (created_at = ? AND id < ?))`), and fetch **`limit + 1`** rows to detect `has_more` without a separate `COUNT(*)`!

```sql
SELECT id, title, published_at
FROM articles
WHERE (published_at < ?) OR (published_at = ? AND id < ?)
ORDER BY published_at DESC, id DESC
LIMIT ?;  -- pass limit + 1
```

### Challenge
Implement `encode_cursor`, `decode_cursor`, and `fetch_feed_page(conn, limit=3, cursor=None)` returning `{"items": [...], "next_cursor": str | None, "has_more": bool}` in `keyset_pagination.py`.
