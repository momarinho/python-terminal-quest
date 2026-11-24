from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from warmup import Account, Base, add_account


def test_add_account_persists_row() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        acc = add_account(session, "ada@example.com", 250)
        assert acc.id is not None
        loaded = session.scalar(select(Account).where(Account.email == "ada@example.com"))
        assert loaded is not None and loaded.balance == 250


def test_add_multiple_accounts() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        a1 = add_account(session, "a@example.com", 10)
        a2 = add_account(session, "b@example.com", 20)
        assert a1.id != a2.id
