from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from warmup import Base, add_account, list_active_emails


def test_add_account_and_list_active_emails() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        a1 = add_account(session, "zoe@example.com", 500)
        add_account(session, "bob@example.com", 50)
        add_account(session, "ana@example.com", 200)
        assert a1.id is not None
        assert list_active_emails(session, 100) == ["ana@example.com", "zoe@example.com"]


def test_list_active_emails_empty_match() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        add_account(session, "bob@example.com", 10)
        assert list_active_emails(session, 999) == []
