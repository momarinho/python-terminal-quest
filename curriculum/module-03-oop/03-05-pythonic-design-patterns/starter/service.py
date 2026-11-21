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
        # TODO: validate invoice_id & subtotal >= 0, apply factory strategy, save via repo
        _ = (create_pricing_strategy, subtotal, strategy_kind, strategy_value)
        return {}
