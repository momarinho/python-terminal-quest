from __future__ import annotations

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)


def add_account(session: Session, email: str, balance: int) -> Account:
    """Create, add, commit, and return an Account row."""
    account = Account(email=email, balance=balance)
    session.add(account)
    session.commit()
    return account


def list_active_emails(session: Session, min_balance: int) -> list[str]:
    """Return sorted emails with balance >= min_balance using SQLAlchemy 2.0 select()."""
    stmt = (
        select(Account.email)
        .where(Account.balance >= min_balance)
        .order_by(Account.email)
    )
    return list(session.scalars(stmt).all())
