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
    # TODO: update wallet, use session.begin_nested() for AuditEntry catching IntegrityError
    _ = (IntegrityError, AuditEntry, Wallet, session, wallet_id, amount_cents, audit_note)
    return False


def update_wallet_stale_safe(session: Session, wallet: Wallet, delta_cents: int) -> int:
    """Apply `delta_cents` and flush, converting StaleDataError into WalletConflictError."""
    # TODO: mutate wallet, flush, catch StaleDataError -> raise WalletConflictError from exc
    _ = (StaleDataError, session, delta_cents)
    return wallet.balance_cents
