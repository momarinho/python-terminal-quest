from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from domain import Receipt


class PaymentGatewayPort(Protocol):
    def charge(self, account_id: str, total: Decimal, secret: str) -> str: ...


class ReceiptRepoPort(Protocol):
    def save(self, receipt: Receipt) -> None: ...
    def get(self, receipt_id: str) -> Receipt | None: ...
