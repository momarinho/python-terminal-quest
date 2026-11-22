from models import Base, Buyer, Order, OrderItem
from repository import count_queries, fetch_high_volume_orders, fetch_orders_summary
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session


def test_fetch_orders_summary_executes_at_most_two_queries() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        for i in range(1, 26):
            buyer = Buyer(name=f"Buyer-{i}")
            order = Order(
                buyer=buyer,
                items=[OrderItem(sku=f"SKU-{i}-A", qty=1), OrderItem(sku=f"SKU-{i}-B", qty=2)],
            )
            session.add(order)

    queries: list[str] = []

    def _count_sql(_conn: object, _cursor: object, statement: str, *_args: object) -> None:
        queries.append(statement)

    event.listen(engine, "before_cursor_execute", _count_sql)
    try:
        with Session(engine) as session:
            rows = fetch_orders_summary(session, limit=25)
    finally:
        event.remove(engine, "before_cursor_execute", _count_sql)

    assert len(rows) == 25
    assert rows[0]["buyer"] == "Buyer-1"
    assert rows[0]["item_skus"] == ["SKU-1-A", "SKU-1-B"]
    assert len(queries) <= 2, f"Expected <= 2 SQL queries (zero-N+1), got {len(queries)}"


def test_count_queries_and_high_volume_orders() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        buyer = Buyer(name="Acme")
        session.add_all([
            Order(buyer=buyer, items=[OrderItem(sku="A1", qty=1)]),
            Order(buyer=buyer, items=[OrderItem(sku="B2", qty=4), OrderItem(sku="B3", qty=3)]),
            Order(buyer=buyer, items=[OrderItem(sku="C3", qty=5)]),
        ])

    with count_queries(engine) as recorded, Session(engine) as session:
        high = fetch_high_volume_orders(session, min_total_qty=5, limit=10)
        assert len(recorded) <= 2

    assert len(recorded) >= 1
    assert [row["total_qty"] for row in high] == [7, 5]
    assert high[0]["item_skus"] == ["B2", "B3"]


def test_fetch_orders_summary_respects_limit_and_empty_db() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        assert fetch_orders_summary(session, limit=10) == []

    with Session(engine) as session, session.begin():
        buyer = Buyer(name="Acme")
        session.add_all([
            Order(buyer=buyer, items=[OrderItem(sku="A1", qty=1)]),
            Order(buyer=buyer, items=[OrderItem(sku="B2", qty=2)]),
            Order(buyer=buyer, items=[OrderItem(sku="C3", qty=3)]),
        ])

    with Session(engine) as session:
        limited = fetch_orders_summary(session, limit=2)
        assert len(limited) == 2
        assert [row["item_skus"] for row in limited] == [["A1"], ["B2"]]
