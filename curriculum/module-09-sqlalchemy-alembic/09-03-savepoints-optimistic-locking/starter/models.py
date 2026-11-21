from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance_cents: Mapped[int]
    version: Mapped[int] = mapped_column(nullable=False, default=1)
    # TODO: enable SQLAlchemy optimistic locking via __mapper_args__ = {"version_id_col": version}


class AuditEntry(Base):
    __tablename__ = "audit_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int]
    note: Mapped[str] = mapped_column(String(120), nullable=False)
