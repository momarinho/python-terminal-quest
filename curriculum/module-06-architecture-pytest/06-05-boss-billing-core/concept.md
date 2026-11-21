## Boss Fight: Multi-Module Billing Core

Assemble a clean 4-file hexagonal billing core with **zero** circular imports and strict validation at the boundary.

### Architecture (`config.py`, `domain.py`, `ports.py`, `service.py`)
1. **`config.py` -> `BillingSettings(BaseSettings)`**
   * `env_prefix = "BILLING_"`
   * `gateway_secret: SecretStr` (non-empty), `tax_rate: Decimal = Field(default=Decimal("0.10"), ge=Decimal("0"), lt=Decimal("1"))`.
2. **`domain.py` -> Pydantic v2 Discriminated Union & Result**
   * `SubscriptionCharge`: `kind: Literal["subscription"]`, `account_id: str` (non-blank), `plan_price: Decimal` (`> 0`), `seats: int` (`>= 1`).
   * `UsageCharge`: `kind: Literal["usage"]`, `account_id: str` (non-blank), `units: int` (`>= 1`), `unit_price: Decimal` (`> 0`).
   * `ChargeCommand = Annotated[SubscriptionCharge | UsageCharge, Field(discriminator="kind")]`.
   * `Receipt`: `receipt_id: str`, `account_id: str`, `subtotal: Decimal`, `tax: Decimal`, `total: Decimal`.
3. **`ports.py` -> Structural Protocols (`TYPE_CHECKING` safe)**
   * `PaymentGatewayPort`: `charge(self, account_id: str, total: Decimal, secret: str) -> str` (returns transaction reference).
   * `ReceiptRepoPort`: `save(self, receipt: Receipt) -> None` and `get(self, receipt_id: str) -> Receipt | None`.
4. **`service.py` -> `BillingOrchestrator(settings, gateway, repo)`**
   * `process(raw_command: dict[str, object]) -> dict[str, object]`:
     * Validate `raw_command` into `ChargeCommand` via `TypeAdapter(ChargeCommand).validate_python(raw_command)`.
     * Compute exact `Decimal` subtotal (`plan_price * seats` or `units * unit_price`), `tax = (subtotal * settings.tax_rate).quantize(Decimal("0.01"), ROUND_HALF_UP)`, `total = subtotal + tax`.
     * Call `gateway.charge(cmd.account_id, total, settings.gateway_secret.get_secret_value())` -> `receipt_id`.
     * Construct `Receipt`, save to `repo`, and return `receipt.model_dump(mode="json")`.
