from collections.abc import Iterator
from contextlib import contextmanager

from models import Order
from sqlalchemy import Engine, event, select
from sqlalchemy.orm import Session, joinedload, selectinload


@contextmanager
def count_queries(engine: Engine) -> Iterator[list[str]]:
    """Context manager recording executed SQL statements on `engine` via before_cursor_execute."""
    queries: list[str] = []

    def _listener(_conn: object, _cursor: object, statement: str, *_args: object) -> None:
        queries.append(statement)

    event.listen(engine, "before_cursor_execute", _listener)
    try:
        yield queries
    finally:
        event.remove(engine, "before_cursor_execute", _listener)


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


def fetch_high_volume_orders(
    session: Session,
    min_total_qty: int,
    limit: int = 25,
) -> list[dict[str, object]]:
    """Return eager-loaded orders with total_qty >= min_total_qty in <= 2 SQL queries."""
    stmt = (
        select(Order)
        .options(joinedload(Order.buyer), selectinload(Order.items))
        .order_by(Order.id)
        .limit(limit)
    )
    orders = session.scalars(stmt).unique().all()
    results: list[dict[str, object]] = []
    for order in orders:
        total_qty = sum(it.qty for it in order.items)
        if total_qty >= min_total_qty:
            results.append(
                {
                    "order_id": order.id,
                    "buyer": order.buyer.name,
                    "total_qty": total_qty,
                    "item_skus": [it.sku for it in order.items],
                }
            )
    return results
