import pytest
from pydantic import ValidationError
from warmup import ServiceItem, dump_service_dict, validate_service


def test_validate_and_dump_service() -> None:
    item = validate_service({"name": "billing", "port": "8080"})
    assert item == ServiceItem(name="billing", port=8080)
    assert dump_service_dict(item) == {"name": "billing", "port": 8080}


def test_port_out_of_range_fails() -> None:
    with pytest.raises(ValidationError):
        validate_service({"name": "billing", "port": 70000})
