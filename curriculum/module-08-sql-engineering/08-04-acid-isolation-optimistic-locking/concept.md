## Concept: ACID Transactions, Isolation & Optimistic Locking

Reading a balance in Python, modifying it, and writing it back without concurrency protection causes **lost updates** under concurrent requests.

### Optimistic Locking vs. Pessimistic Row Locks
* **Optimistic Concurrency Control:** Include a `version` integer column and check it inside the `UPDATE`:
  ```sql
  UPDATE seat_bookings
  SET holder = ?, version = version + 1
  WHERE seat_id = ? AND version = ?;
  ```
  If `cursor.rowcount == 0`, another transaction updated the row first—raise a domain conflict error!
* **PostgreSQL vs. SQLite:** PostgreSQL uses **MVCC** (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`) and supports `SELECT ... FOR UPDATE SKIP LOCKED` for distributed job queues, whereas SQLite serializes writes via `BEGIN IMMEDIATE` transactions.

### Challenge
Implement `InsufficientFundsError`, `OptimisticConflictError`, `transfer_balance_atomic`, and `update_tier_optimistic` in `transactions.py` (with `isolation_level=None` explicit `BEGIN IMMEDIATE` / `COMMIT` / `ROLLBACK`).
