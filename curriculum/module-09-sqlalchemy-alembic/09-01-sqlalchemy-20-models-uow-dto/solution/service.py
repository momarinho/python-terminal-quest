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
    clean_email = email.strip().lower()
    clean_plan = plan.strip().lower()
    if not clean_email or not clean_plan:
        raise ValueError("email and plan must not be blank")

    with Session(engine) as session, session.begin():
        customer = Customer(
            email=clean_email,
            subscriptions=[Subscription(plan=clean_plan, active=True)],
        )
        session.add(customer)
        session.flush()
        return CustomerDTO.model_validate(customer)


def get_customer_summary(engine: Engine, customer_id: int) -> CustomerDTO | None:
    """Fetch Customer + subscriptions eagerly and map to CustomerDTO (or None)."""
    with Session(engine) as session:
        stmt = (
            select(Customer)
            .options(selectinload(Customer.subscriptions))
            .where(Customer.id == customer_id)
        )
        customer = session.scalars(stmt).first()
        if customer is None:
            return None
        return CustomerDTO.model_validate(customer)
