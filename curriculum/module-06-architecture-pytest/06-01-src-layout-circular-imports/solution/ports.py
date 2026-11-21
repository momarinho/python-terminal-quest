from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from domain import ShipmentOrder


class CarrierPort(Protocol):
    def book_shipment(self, order: ShipmentOrder) -> str: ...
