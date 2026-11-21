import pytest
from models import Base
from schemas import CustomerDTO
from service import get_customer_summary, register_customer_with_subscription
from sqlalchemy import create_engine


def test_register_and_fetch_returns_detached_safe_pydantic_dto() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    dto = register_customer_with_subscription(engine, "  Ana@Acme.DEV ", "pro")
    assert isinstance(dto, CustomerDTO)
    assert dto.email == "ana@acme.dev"
    assert len(dto.subscriptions) == 1
    assert dto.subscriptions[0].plan == "pro"

    fetched = get_customer_summary(engine, dto.id)
    assert fetched == dto
    assert get_customer_summary(engine, 999) is None


def test_rejects_blank_inputs() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with pytest.raises(ValueError):
        register_customer_with_subscription(engine, "   ", "pro")
