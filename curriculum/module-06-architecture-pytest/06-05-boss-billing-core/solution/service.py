from decimal import ROUND_HALF_UP, Decimal

from config import BillingSettings
from domain import ChargeCommand, Receipt, SubscriptionCharge
from ports import PaymentGatewayPort, ReceiptRepoPort
from pydantic import TypeAdapter

_CENT = Decimal("0.01")
_COMMAND_ADAPTER = TypeAdapter(ChargeCommand)


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
        cmd = _COMMAND_ADAPTER.validate_python(raw_command)
        if isinstance(cmd, SubscriptionCharge):
            raw_subtotal = cmd.plan_price * cmd.seats
        else:
            raw_subtotal = cmd.unit_price * cmd.units

        subtotal = raw_subtotal.quantize(_CENT, rounding=ROUND_HALF_UP)
        tax = (subtotal * self.settings.tax_rate).quantize(_CENT, rounding=ROUND_HALF_UP)
        total = subtotal + tax

        receipt_id = self.gateway.charge(
            cmd.account_id,
            total,
            self.settings.gateway_secret.get_secret_value(),
        )
        receipt = Receipt(
            receipt_id=receipt_id,
            account_id=cmd.account_id,
            subtotal=subtotal,
            tax=tax,
            total=total,
        )
        self.repo.save(receipt)
        return receipt.model_dump(mode="json")
