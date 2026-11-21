import sqlite3

from sql_analytics import customers_without_refunds, high_value_customers


def _seed_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            amount_cents INTEGER NOT NULL,
            status TEXT NOT NULL
        );
        CREATE TABLE refunds (id INTEGER PRIMARY KEY, customer_id INTEGER);

        INSERT INTO customers VALUES (1, 'Ana'), (2, 'Bruno'), (3, 'Carla');
        INSERT INTO orders VALUES
            (1, 1, 5000, 'PAID'),
            (2, 1, 3000, 'PAID'),
            (3, 1, 9000, 'CANCELLED'),
            (4, 2, 8000, 'PAID'),
            (5, 3, 2000, 'PAID');
        INSERT INTO refunds VALUES (10, 2), (11, NULL);
        """
    )
    return conn


def test_high_value_customers_excludes_cancelled_and_sorts() -> None:
    conn = _seed_db()
    assert high_value_customers(conn, 8000) == [
        {"customer_id": 1, "name": "Ana", "total_cents": 8000, "order_count": 2},
        {"customer_id": 2, "name": "Bruno", "total_cents": 8000, "order_count": 1},
    ]


def test_customers_without_refunds_is_null_safe() -> None:
    conn = _seed_db()
    # refunds contains a NULL customer_id row which breaks naive NOT IN!
    assert customers_without_refunds(conn) == [1, 3]
