from models import Order
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload


def fetch_orders_summary(session: Session, limit: int = 25) -> list[dict[str, object]]:
    """Load orders + buyer + items without N+1 queries and return serialized summary dicts."""
    stmt = (
        select(Order)
        .options(joinedload(Order.buyer), selectinload(Order.items))
        .order_by(Order.id)
        .limit(limit)
    )
    orders = session.scalars(stmt).unique().all()
    return [
        {
            "order_id": o.id,
            "buyer": o.buyer.name,
            "item_skus": [it.sku for it in o.items],
        }
        for o in orders
    ]
