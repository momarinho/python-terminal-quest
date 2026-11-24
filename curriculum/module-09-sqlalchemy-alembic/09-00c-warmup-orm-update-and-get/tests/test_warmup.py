from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from warmup import Account, Base, credit_account


def test_credit_account_updates_balance() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        acc = Account(email="ada@example.com", balance=100)
        session.add(acc)
        session.commit()
        updated = credit_account(session, acc.id, 45)
        assert updated is not None and updated.balance == 145


def test_credit_account_missing_returns_none() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        assert credit_account(session, 999, 10) is None
