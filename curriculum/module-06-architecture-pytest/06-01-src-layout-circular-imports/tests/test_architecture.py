from domain import ShipmentOrder
from ports import CarrierPort
from service import DispatchService


class FakeCarrier:
    def __init__(self) -> None:
        self.booked: list[ShipmentOrder] = []

    def book_shipment(self, order: ShipmentOrder) -> str:
        self.booked.append(order)
        return f"TRK-{order.order_id}"


def test_unidirectional_imports_and_dispatch() -> None:
    carrier = FakeCarrier()
    svc = DispatchService(carrier)
    order, tracking = svc.dispatch("ORD-42", "Berlin")
    assert order == ShipmentOrder("ORD-42", "Berlin", "DISPATCHED")
    assert tracking == "TRK-ORD-42"
    assert carrier.booked == [order]


def test_ports_exposes_carrier_protocol() -> None:
    assert hasattr(CarrierPort, "book_shipment")
