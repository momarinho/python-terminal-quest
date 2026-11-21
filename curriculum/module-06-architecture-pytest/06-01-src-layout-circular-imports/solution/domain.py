from dataclasses import dataclass


@dataclass(frozen=True)
class ShipmentOrder:
    order_id: str
    destination: str
    status: str = "DISPATCHED"

    def __post_init__(self) -> None:
        if not self.order_id.strip() or not self.destination.strip():
            raise ValueError("order_id and destination must be non-empty")
