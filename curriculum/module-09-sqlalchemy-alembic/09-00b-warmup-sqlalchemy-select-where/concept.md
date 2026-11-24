## Beginner Warm-Up 2: SQLAlchemy 2.0 `select()`

Construct SQL expressions directly from mapped attributes (`Account.balance >= min_balance`) and execute via `session.scalars(stmt)`:

```python
def list_active_emails(session: Session, min_balance: int) -> list[str]:
    stmt = (
        select(Account.email)
        .where(Account.balance >= min_balance)
        .order_by(Account.email)
    )
    return list(session.scalars(stmt).all())
```

### Challenge
Implement `list_active_emails` in `warmup.py`.
