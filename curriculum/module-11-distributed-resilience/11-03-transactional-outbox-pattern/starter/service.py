from __future__ import annotations

import sqlite3


class InvoiceService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def issue_invoice(self, invoice_id: str, customer_id: str, amount_cents: int) -> str:
        """Persist invoice + PENDING outbox event atomically and return event_id."""
        # TODO: Validate amount_cents > 0, then insert into invoices AND outbox_events
        # inside one atomic `with self._conn:` transaction.
        raise NotImplementedError("TODO: issue_invoice with atomic outbox write")
