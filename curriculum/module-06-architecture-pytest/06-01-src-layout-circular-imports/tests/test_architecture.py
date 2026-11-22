import pytest
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
    order, tracking = svc.dispatch(" ORD-42 ", " Berlin ")
    assert order == ShipmentOrder("ORD-42", "Berlin", "DISPATCHED")
    assert tracking == "TRK-ORD-42"
    assert carrier.booked == [order]


def test_shipment_order_validation_and_batch_history() -> None:
    with pytest.raises(ValueError):
        ShipmentOrder("   ", "Berlin")
    with pytest.raises(ValueError):
        ShipmentOrder("ORD-1", "")

    carrier = FakeCarrier()
    svc = DispatchService(carrier)
    results = svc.dispatch_batch([("ORD-1", "Lisbon"), ("ORD-2", "Tokyo")])
    assert [r[1] for r in results] == ["TRK-ORD-1", "TRK-ORD-2"]
    assert svc.booked_history() == [("ORD-1", "TRK-ORD-1"), ("ORD-2", "TRK-ORD-2")]


def test_ports_exposes_carrier_protocol() -> None:
    assert hasattr(CarrierPort, "book_shipment")
