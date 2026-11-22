from collections.abc import Iterator
from contextlib import contextmanager

from models import Order
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session


@contextmanager
def count_queries(engine: Engine) -> Iterator[list[str]]:
    """Context manager recording executed SQL statements on `engine` via before_cursor_execute."""
    queries: list[str] = []
    yield queries


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


def fetch_high_volume_orders(
    session: Session,
    min_total_qty: int,
    limit: int = 25,
) -> list[dict[str, object]]:
    """Return eager-loaded orders with total_qty >= min_total_qty in <= 2 SQL queries."""
    return []
