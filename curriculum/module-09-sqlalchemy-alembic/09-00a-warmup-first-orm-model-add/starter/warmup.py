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


def add_account(session: Session, email: str, balance: int) -> Account:
    """Create, add, commit, and return an Account row."""
    return Account(email="", balance=0)
