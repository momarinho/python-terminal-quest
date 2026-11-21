from config import BillingSettings
from domain import ChargeCommand, Receipt
from ports import PaymentGatewayPort, ReceiptRepoPort


class BillingOrchestrator:
    def __init__(
        self,
        settings: BillingSettings,
        gateway: PaymentGatewayPort,
        repo: ReceiptRepoPort,
    ) -> None:
        self.settings = settings
        self.gateway = gateway
        self.repo = repo

    def process(self, raw_command: dict[str, object]) -> dict[str, object]:
        # TODO: validate ChargeCommand via TypeAdapter, compute Decimal subtotal/tax/total,
        # charge gateway, save Receipt, return receipt.model_dump(mode="json")
        _ = (ChargeCommand, Receipt, raw_command)
        return {}
