from __future__ import annotations

import json
import sqlite3


class InvoiceService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def issue_invoice(self, invoice_id: str, customer_id: str, amount_cents: int) -> str:
        """Persist invoice + PENDING outbox event atomically and return event_id."""
        if amount_cents <= 0:
            raise ValueError("amount_cents must be positive")
        event_id = f"evt-{invoice_id}"
        payload = json.dumps(
            {
                "invoice_id": invoice_id,
                "customer_id": customer_id,
                "amount_cents": amount_cents,
            },
            sort_keys=True,
        )
        with self._conn:
            self._conn.execute(
                "INSERT INTO invoices (id, customer_id, amount_cents, status) VALUES (?, ?, ?, ?)",
                (invoice_id, customer_id, amount_cents, "ISSUED"),
            )
            self._conn.execute(
                """
                INSERT INTO outbox_events (id, aggregate_type, aggregate_id, event_type, payload_json, status)
                VALUES (?, ?, ?, ?, ?, 'PENDING')
                """,
                (event_id, "invoice", invoice_id, "InvoiceIssued", payload),
            )
        return event_id
