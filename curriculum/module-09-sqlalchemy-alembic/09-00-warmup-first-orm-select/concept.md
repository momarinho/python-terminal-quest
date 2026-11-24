## Concept: Warm-Up & Quick Syntax Reveal (Module 9)

SQLAlchemy 2.0 replaces legacy `.query()` calls with clean, type-safe `select(...)` statements executed through `session.scalars(...)`.

### Pattern Reveal #1 — Persisting an ORM Row
```python
def add_account(session: Session, email: str, balance: int) -> Account:
    account = Account(email=email, balance=balance)
    session.add(account)
    session.commit()
    return account
```

### Pattern Reveal #2 — Typed `select()` with `.where()` & `.order_by()`
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
`Account(Base)` is already defined in `warmup.py`. Complete `add_account` and `list_active_emails`.
