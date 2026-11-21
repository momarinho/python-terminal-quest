from models import Customer, Subscription
from schemas import CustomerDTO
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, selectinload


def register_customer_with_subscription(
    engine: Engine,
    email: str,
    plan: str,
) -> CustomerDTO:
    """Create Customer + initial Subscription in one Unit of Work and return a detached-safe DTO."""
    # TODO: use Session(engine) + session.begin(), validate non-blank email/plan, return CustomerDTO
    _ = (Session, select, selectinload, Customer, Subscription, email, plan)
    return CustomerDTO(id=0, email="", subscriptions=[])


def get_customer_summary(engine: Engine, customer_id: int) -> CustomerDTO | None:
    """Fetch Customer + subscriptions eagerly and map to CustomerDTO (or None)."""
    # TODO: select(Customer).options(selectinload(Customer.subscriptions)).where(Customer.id == customer_id)
    return None
