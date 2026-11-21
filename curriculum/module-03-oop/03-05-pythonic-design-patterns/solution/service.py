from decimal import Decimal

from patterns import InvoiceRepository, create_pricing_strategy


class BillingService:
    def __init__(self, repo: InvoiceRepository) -> None:
        self.repo = repo

    def create_invoice(
        self,
        invoice_id: str,
        subtotal: Decimal,
        strategy_kind: str = "none",
        strategy_value: str = "0",
    ) -> dict[str, object]:
        cleaned_id = invoice_id.strip()
        if not cleaned_id:
            raise ValueError("invoice_id must not be blank")
        if subtotal < 0:
            raise ValueError("subtotal must be non-negative")

        strategy = create_pricing_strategy(strategy_kind, strategy_value)
        total = strategy.apply(subtotal)
        record: dict[str, object] = {
            "id": cleaned_id,
            "subtotal": subtotal,
            "total": total,
        }
        self.repo.save(cleaned_id, record)
        return record
