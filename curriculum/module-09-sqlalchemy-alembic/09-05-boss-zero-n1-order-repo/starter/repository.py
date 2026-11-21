from models import Order, OrderLine, Product
from schemas import OrderDTO
from sqlalchemy.orm import Session


class InsufficientStockError(Exception):
    """Raised when requested quantity exceeds available product stock."""


class OrderConflictError(Exception):
    """Raised on optimistic lock conflict during order placement."""


def place_order(
    session: Session,
    customer_email: str,
    items: list[tuple[str, int]],
) -> OrderDTO:
    """Validate items, decrement product stock with optimistic lock, create Order, return OrderDTO."""
    # TODO: implement atomic order placement catching StaleDataError -> OrderConflictError
    _ = (Order, OrderLine, Product, session, customer_email, items)
    return OrderDTO(id=0, customer_email="", status="CONFIRMED", lines=[])


def list_orders_dto(
    session: Session,
    status: str | None = None,
    limit: int = 50,
) -> list[OrderDTO]:
    """List orders + lines in <= 2 SQL queries (zero-N+1) mapped to OrderDTO."""
    # TODO: use selectinload(Order.lines), optional status filter, limit
    return []
