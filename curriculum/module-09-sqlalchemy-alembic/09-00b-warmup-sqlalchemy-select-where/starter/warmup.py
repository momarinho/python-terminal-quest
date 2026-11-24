from __future__ import annotations

from sqlalchemy import Integer, String, select  # noqa: F401
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)


def list_active_emails(session: Session, min_balance: int) -> list[str]:
    """Return sorted emails where balance >= min_balance."""
    return []
