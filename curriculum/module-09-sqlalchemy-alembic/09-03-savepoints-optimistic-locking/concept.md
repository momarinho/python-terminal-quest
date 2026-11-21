## Concept: Savepoints (`begin_nested`) & Optimistic Locking (`version_id_col`)

SQLAlchemy 2.0 provides two essential concurrency & reliability primitives inside `Session`:

### 1. Savepoints with `session.begin_nested()`
When an optional side-step (like writing a secondary tag or metric row) fails inside an outer transaction, catching the error around `with session.begin_nested():` rolls back **only** the inner savepoint—preserving the outer transaction's work!

```python
with session.begin():
    lot = session.get(InventoryLot, lot_id)
    lot.qty += 10
    try:
        with session.begin_nested():
            session.add(TagRecord(tag=None))  # violates NOT NULL
    except IntegrityError:
        pass  # outer lot update still commits cleanly!
```

### 2. Optimistic Locking via `version_id_col`
Configure `__mapper_args__ = {"version_id_col": version}` on your model. Whenever SQLAlchemy flushes an `UPDATE` or `DELETE`, it automatically appends `WHERE version = <loaded_version>`—raising `StaleDataError` if another transaction modified the row concurrently!

### Challenge
Configure `version_id_col` on `Wallet` in `models.py`, and implement `credit_with_optional_audit` (using `begin_nested()`) and `update_wallet_stale_safe` (catching `StaleDataError` -> `WalletConflictError`) in `service.py`.
