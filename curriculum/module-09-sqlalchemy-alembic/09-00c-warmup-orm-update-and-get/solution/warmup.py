from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)


def credit_account(session: Session, account_id: int, delta: int) -> Account | None:
    """Add delta to Account balance by ID, or return None if missing."""
    account = session.get(Account, account_id)
    if account is None:
        return None
    account.balance += delta
    session.commit()
    return account
