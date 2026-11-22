from domain import ShipmentOrder
from ports import CarrierPort


class DispatchService:
    def __init__(self, carrier: CarrierPort) -> None:
        self.carrier = carrier
        self._history: list[tuple[str, str]] = []

    def dispatch(self, order_id: str, destination: str) -> tuple[ShipmentOrder, str]:
        """Strip inputs, build ShipmentOrder, book via carrier, record history, and return (order, tracking)."""
        order = ShipmentOrder(order_id=order_id.strip(), destination=destination.strip())
        tracking_code = self.carrier.book_shipment(order)
        self._history.append((order.order_id, tracking_code))
        return order, tracking_code

    def dispatch_batch(self, items: list[tuple[str, str]]) -> list[tuple[ShipmentOrder, str]]:
        """Dispatch each (order_id, destination) item in order."""
        return [self.dispatch(order_id, destination) for order_id, destination in items]

    def booked_history(self) -> list[tuple[str, str]]:
        """Return recorded [(order_id, tracking_code), ...] in dispatch order."""
        return list(self._history)
