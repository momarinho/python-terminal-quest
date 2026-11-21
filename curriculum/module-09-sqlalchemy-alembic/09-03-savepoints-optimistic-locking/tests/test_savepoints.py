import pytest
from models import AuditEntry, Base, Wallet
from service import (
    WalletConflictError,
    credit_with_optional_audit,
    update_wallet_stale_safe,
)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def test_savepoint_rolls_back_failed_audit_while_preserving_credit() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        session.add(Wallet(id=1, balance_cents=1000))

    with Session(engine) as session, session.begin():
        audit_ok = credit_with_optional_audit(session, 1, 500, audit_note=None)
        assert audit_ok is False

    with Session(engine) as session:
        wallet = session.get(Wallet, 1)
        assert wallet is not None and wallet.balance_cents == 1500
        assert session.scalars(select(AuditEntry)).all() == []


def test_optimistic_locking_raises_wallet_conflict_error_on_stale_version() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        session.add(Wallet(id=1, balance_cents=1000))

    s1 = Session(engine)
    s2 = Session(engine)
    try:
        w1 = s1.get(Wallet, 1)
        w2 = s2.get(Wallet, 1)
        assert w1 is not None and w2 is not None

        update_wallet_stale_safe(s1, w1, 200)
        s1.commit()

        with pytest.raises(WalletConflictError):
            update_wallet_stale_safe(s2, w2, 300)
    finally:
        s1.close()
        s2.close()
