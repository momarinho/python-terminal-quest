import pytest
from config_parser import parse_service_config


def test_parses_valid_config_and_types() -> None:
    cfg = parse_service_config("  auth-api ", " 8443 ", "2.5", "TRUE", " us-east-1 ")
    assert cfg["service_name"] == "auth-api"
    assert cfg["port"] == 8443 and type(cfg["port"]) is int
    assert cfg["timeout_sec"] == 2.5 and type(cfg["timeout_sec"]) is float
    assert cfg["tls_enabled"] is True
    assert cfg["region"] == "us-east-1"


def test_false_string_does_not_evaluate_truthy() -> None:
    cfg = parse_service_config("worker", "9000", "1.0", "false", "   ")
    assert cfg["tls_enabled"] is False
    assert cfg["region"] is None


def test_rejects_invalid_port_timeout_or_bool() -> None:
    with pytest.raises(ValueError):
        parse_service_config("api", "70000", "1.0", "true")
    with pytest.raises(ValueError):
        parse_service_config("api", "8080", "0", "yes")
    with pytest.raises(ValueError):
        parse_service_config("api", "8080", "1.0", "maybe")
    with pytest.raises(ValueError):
        parse_service_config("   ", "8080", "1.0", "on")
