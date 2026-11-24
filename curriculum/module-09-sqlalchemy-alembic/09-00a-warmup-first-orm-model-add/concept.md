## Beginner Warm-Up 1: Persisting an ORM Row

SQLAlchemy 2.0 maps Python classes cleanly to SQL tables using `Mapped[...]` and `mapped_column(...)`:

```python
def add_account(session: Session, email: str, balance: int) -> Account:
    account = Account(email=email, balance=balance)
    session.add(account)
    session.commit()
    return account
```

### Challenge
`Base` and `Account` are already set up in `warmup.py`. Complete `add_account`.
