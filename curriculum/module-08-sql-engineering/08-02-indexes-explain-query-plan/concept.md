## Concept: Composite Indexes & `EXPLAIN QUERY PLAN`

Full table scans (`SCAN table`) grow linearly $O(N)$ as rows accumulate. A well-ordered B-tree **composite index** turns equality + range/sort queries into $O(\log N)$ index seeks (`SEARCH table USING INDEX ...`).

### Leftmost-Prefix & Equality-First Rule
For a query filtering `WHERE branch_id = ? AND status = ? ORDER BY due_at DESC LIMIT 20`:
* Put **equality** columns first (`branch_id, status`), followed by the **sort/range** column (`due_at DESC`).
* **SQLite vs. PostgreSQL:** In SQLite, inspect plans with `EXPLAIN QUERY PLAN <sql>`; in PostgreSQL, run `EXPLAIN (ANALYZE, BUFFERS) <sql>` to verify `Index Scan` / `Index Only Scan` and buffer hits.

```sql
CREATE INDEX IF NOT EXISTS idx_loans_branch_status_due
ON library_loans (branch_id, status, due_at DESC);
```

### Challenge
Implement `create_audit_index(conn)`, `fetch_recent_alerts(conn, tenant_id, severity, limit)`, and `explain_alerts_plan(conn, tenant_id, severity, limit)` in `index_tuning.py` so `EXPLAIN QUERY PLAN` uses `SEARCH ... USING INDEX` with zero `SCAN`.
