from domain import ShipmentOrder
from ports import CarrierPort


class DispatchService:
    def __init__(self, carrier: CarrierPort) -> None:
        self.carrier = carrier

    def dispatch(self, order_id: str, destination: str) -> tuple[ShipmentOrder, str]:
        order = ShipmentOrder(order_id=order_id.strip(), destination=destination.strip())
        tracking_code = self.carrier.book_shipment(order)
        return order, tracking_code
