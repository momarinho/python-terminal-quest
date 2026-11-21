from models import Order, OrderLine, Product
from schemas import OrderDTO
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.exc import StaleDataError


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
    clean_email = customer_email.strip().lower()
    if not clean_email or not items:
        raise ValueError("customer_email and non-empty items are required")
    if any(qty <= 0 or not sku.strip() for sku, qty in items):
        raise ValueError("Every item requires non-blank sku and positive qty")

    skus = {sku.strip() for sku, _ in items}
    products = {
        p.sku: p
        for p in session.scalars(select(Product).where(Product.sku.in_(skus))).all()
    }

    order_lines: list[OrderLine] = []
    for raw_sku, qty in items:
        sku = raw_sku.strip()
        product = products.get(sku)
        if product is None:
            raise ValueError(f"Unknown SKU: {sku}")
        if product.stock < qty:
            raise InsufficientStockError(f"Insufficient stock for {sku}")
        product.stock -= qty
        order_lines.append(OrderLine(sku=sku, qty=qty))

    order = Order(customer_email=clean_email, status="CONFIRMED", lines=order_lines)
    session.add(order)
    try:
        session.flush()
    except StaleDataError as exc:
        raise OrderConflictError("Optimistic lock conflict placing order") from exc

    return OrderDTO.model_validate(order)


def list_orders_dto(
    session: Session,
    status: str | None = None,
    limit: int = 50,
) -> list[OrderDTO]:
    """List orders + lines in <= 2 SQL queries (zero-N+1) mapped to OrderDTO."""
    stmt = select(Order).options(selectinload(Order.lines)).order_by(Order.id).limit(limit)
    if status is not None:
        stmt = stmt.where(Order.status == status)
    orders = session.scalars(stmt).all()
    return [OrderDTO.model_validate(order) for order in orders]
