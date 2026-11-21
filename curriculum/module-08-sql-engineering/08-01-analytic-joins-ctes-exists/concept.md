## Concept: Analytic SQL (`JOIN`, `GROUP BY`, `HAVING`, CTEs & `EXISTS`)

Raw SQL remains essential whenever ORMs generate N+1 queries or slow subqueries.

### 1NF–3NF Normalization vs. Denormalization
* **1NF:** Atomic column values (no comma-separated lists).
* **2NF / 3NF:** Every non-key column depends on the **whole** primary key and **only** the primary key (eliminating update anomalies).
* **Controlled Denormalization:** Occasionally pre-computing summary columns (`order_total_cents`) for read-heavy dashboards when joins become a measured bottleneck.

### Why `NOT EXISTS` Beats `NOT IN`
If a subquery used with `NOT IN (SELECT ...)` returns **even one `NULL`**, the entire `NOT IN` predicate evaluates to `UNKNOWN` and returns **zero rows**! `NOT EXISTS` handles `NULL` safely and short-circuits on the first match.

```sql
WITH completed_enrollments AS (
    SELECT student_id, COUNT(*) AS course_count
    FROM enrollments
    WHERE status = 'COMPLETED'
    GROUP BY student_id
    HAVING COUNT(*) >= 2
)
SELECT s.name, c.course_count
FROM students s
JOIN completed_enrollments c ON c.student_id = s.id
WHERE NOT EXISTS (
    SELECT 1 FROM suspensions sp WHERE sp.student_id = s.id
);
```

### Challenge
Implement `high_value_customers(conn, min_total_cents)` (CTE + `JOIN` + `GROUP BY` + `HAVING` excluding `"CANCELLED"` orders, sorted by `total_cents DESC, customer_id ASC`) and `customers_without_refunds(conn)` (using `NOT EXISTS` so NULL `refunds.customer_id` rows never poison results) in `sql_analytics.py`.
