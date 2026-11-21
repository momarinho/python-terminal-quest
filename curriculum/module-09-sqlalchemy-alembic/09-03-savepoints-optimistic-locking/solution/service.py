from models import AuditEntry, Wallet
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError


class WalletConflictError(Exception):
    """Raised when optimistic version check fails."""


def credit_with_optional_audit(
    session: Session,
    wallet_id: int,
    amount_cents: int,
    audit_note: str | None,
) -> bool:
    """Credit wallet inside outer session; attempt AuditEntry inside a savepoint returning True iff audit saved."""
    wallet = session.get(Wallet, wallet_id)
    if wallet is None:
        raise ValueError(f"Wallet {wallet_id} not found")
    wallet.balance_cents += amount_cents

    try:
        with session.begin_nested():
            session.add(AuditEntry(wallet_id=wallet_id, note=audit_note))  # type: ignore[arg-type]
            session.flush()
        return True
    except IntegrityError:
        return False


def update_wallet_stale_safe(session: Session, wallet: Wallet, delta_cents: int) -> int:
    """Apply `delta_cents` and flush, converting StaleDataError into WalletConflictError."""
    wallet.balance_cents += delta_cents
    try:
        session.flush()
        return wallet.balance_cents
    except StaleDataError as exc:
        raise WalletConflictError("Concurrent modification detected on wallet") from exc
