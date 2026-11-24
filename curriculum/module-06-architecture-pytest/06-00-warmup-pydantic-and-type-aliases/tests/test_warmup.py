import pytest
from pydantic import ValidationError
from warmup import ServiceItem, dump_service_dict, validate_service


def test_validate_service_accepts_valid_payload() -> None:
    item = validate_service({"name": "billing", "port": "8080"})
    assert item == ServiceItem(name="billing", port=8080)


def test_validate_service_rejects_out_of_range_port() -> None:
    with pytest.raises(ValidationError):
        validate_service({"name": "billing", "port": 70000})


def test_dump_service_dict() -> None:
    assert dump_service_dict(ServiceItem(name="auth", port=443)) == {
        "name": "auth",
        "port": 443,
    }
