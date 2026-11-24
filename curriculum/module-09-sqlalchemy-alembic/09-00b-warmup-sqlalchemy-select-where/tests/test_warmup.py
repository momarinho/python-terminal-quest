from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from warmup import Account, Base, list_active_emails


def test_list_active_emails_filters_and_sorts() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([
            Account(email="zoe@example.com", balance=300),
            Account(email="bob@example.com", balance=50),
            Account(email="ana@example.com", balance=150),
        ])
        session.commit()
        assert list_active_emails(session, 100) == ["ana@example.com", "zoe@example.com"]


def test_list_active_emails_none_matching() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Account(email="bob@example.com", balance=10))
        session.commit()
        assert list_active_emails(session, 500) == []
