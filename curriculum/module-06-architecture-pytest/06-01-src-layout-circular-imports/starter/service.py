from domain import ShipmentOrder
from ports import CarrierPort


class DispatchService:
    def __init__(self, carrier: CarrierPort) -> None:
        self.carrier = carrier

    def dispatch(self, order_id: str, destination: str) -> tuple[ShipmentOrder, str]:
        """Strip inputs, build ShipmentOrder, book via carrier, record history, and return (order, tracking)."""
        _ = (ShipmentOrder, order_id, destination)
        return ShipmentOrder("TODO", "TODO"), ""

    def dispatch_batch(self, items: list[tuple[str, str]]) -> list[tuple[ShipmentOrder, str]]:
        """Dispatch each (order_id, destination) item in order."""
        return []

    def booked_history(self) -> list[tuple[str, str]]:
        """Return recorded [(order_id, tracking_code), ...] in dispatch order."""
        return []
