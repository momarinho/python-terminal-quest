from dataclasses import dataclass

# BUG: circular dependency back into service.py causes ImportError!
from service import DispatchService  # noqa: F401


@dataclass(frozen=True)
class ShipmentOrder:
    order_id: str
    destination: str
    status: str = "DISPATCHED"

    # TODO: validate non-empty order_id and destination in __post_init__
