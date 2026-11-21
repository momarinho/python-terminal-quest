from typing import Protocol

from domain import ShipmentOrder


class CarrierPort(Protocol):
    def book_shipment(self, order: ShipmentOrder) -> str: ...
