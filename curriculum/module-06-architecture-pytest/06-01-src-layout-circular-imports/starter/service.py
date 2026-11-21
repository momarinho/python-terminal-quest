from domain import ShipmentOrder
from ports import CarrierPort


class DispatchService:
    def __init__(self, carrier: CarrierPort) -> None:
        self.carrier = carrier

    def dispatch(self, order_id: str, destination: str) -> tuple[ShipmentOrder, str]:
        # TODO: construct ShipmentOrder and delegate booking to self.carrier
        _ = (ShipmentOrder, order_id, destination)
        return ShipmentOrder("TODO", "TODO"), ""
