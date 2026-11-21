from models import Order
from sqlalchemy import select
from sqlalchemy.orm import Session


def fetch_orders_summary(session: Session, limit: int = 25) -> list[dict[str, object]]:
    """Load orders + buyer + items without N+1 queries and return serialized summary dicts."""
    # BUG: missing eager-loading options triggers 1 + 25*2 = 51 queries!
    orders = session.scalars(select(Order).order_by(Order.id).limit(limit)).all()
    return [
        {
            "order_id": o.id,
            "buyer": o.buyer.name,
            "item_skus": [it.sku for it in o.items],
        }
        for o in orders
    ]
