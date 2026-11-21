import pytest
from models import Base, Product
from repository import (
    InsufficientStockError,
    OrderConflictError,
    list_orders_dto,
    place_order,
)
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session


def test_place_order_and_zero_n1_listing() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        session.add_all([Product(sku="KB-1", stock=100), Product(sku="MS-2", stock=100)])

    with Session(engine) as session, session.begin():
        for i in range(25):
            dto = place_order(session, f"user{i}@acme.dev", [("KB-1", 1), ("MS-2", 2)])
            assert dto.status == "CONFIRMED"

    queries: list[str] = []

    def _counter(_c: object, _cur: object, stmt: str, *_args: object) -> None:
        queries.append(stmt)

    event.listen(engine, "before_cursor_execute", _counter)
    try:
        with Session(engine) as session:
            orders = list_orders_dto(session, status="CONFIRMED", limit=25)
    finally:
        event.remove(engine, "before_cursor_execute", _counter)

    assert len(orders) == 25
    assert len(orders[0].lines) == 2
    assert len(queries) <= 2, f"Expected <= 2 queries, got {len(queries)}"


def test_insufficient_stock_and_optimistic_conflict() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        session.add(Product(sku="GPU-1", stock=2))

    with Session(engine) as s1, pytest.raises(InsufficientStockError):
        place_order(s1, "a@b.dev", [("GPU-1", 5)])

    s_a = Session(engine)
    s_b = Session(engine)
    try:
        p_a = s_a.scalars(select(Product).where(Product.sku == "GPU-1")).one()
        p_b = s_b.scalars(select(Product).where(Product.sku == "GPU-1")).one()
        assert p_a.stock == 2 and p_b.stock == 2

        place_order(s_a, "first@b.dev", [("GPU-1", 1)])
        s_a.commit()

        with pytest.raises(OrderConflictError):
            place_order(s_b, "second@b.dev", [("GPU-1", 1)])
    finally:
        s_a.close()
        s_b.close()
