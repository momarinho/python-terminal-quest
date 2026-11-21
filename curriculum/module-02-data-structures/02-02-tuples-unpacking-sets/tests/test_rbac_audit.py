import pytest
from rbac_audit import audit_permission_drift, dedupe_preserve_order, split_route_record


def test_split_route_record_unpacking() -> None:
    assert split_route_record(("billing", "us-east-1", "/pay", "/refund")) == (
        "billing",
        "us-east-1",
        ("/pay", "/refund"),
    )
    assert split_route_record(("auth", "eu-west-1")) == ("auth", "eu-west-1", ())
    with pytest.raises(ValueError):
        split_route_record(("only-one",))


def test_audit_permission_drift() -> None:
    res = audit_permission_drift(
        ["read:users", "write:orders", "read:ledger"],
        ["read:ledger", "admin:root", "read:users"],
    )
    assert res == {
        "missing": ["write:orders"],
        "extra": ["admin:root"],
        "shared": ["read:ledger", "read:users"],
    }


def test_dedupe_preserve_order() -> None:
    assert dedupe_preserve_order(["e3", "e1", "e3", "e2", "e1", "e4"]) == [
        "e3",
        "e1",
        "e2",
        "e4",
    ]
