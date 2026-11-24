## Beginner Warm-Up 3: Primary-Key Lookup & Dirty Tracking

SQLAlchemy tracks changes to attached ORM objects automatically—just assign the new attribute value and call `session.commit()`:

```python
def credit_account(session: Session, account_id: int, delta: int) -> Account | None:
    account = session.get(Account, account_id)
    if account is None:
        return None
    account.balance += delta
    session.commit()
    return account
```

### Challenge
Implement `credit_account` in `warmup.py`.
