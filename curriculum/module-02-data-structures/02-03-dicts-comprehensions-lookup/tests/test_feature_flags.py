import pytest
from feature_flags import (
    diff_flag_snapshots,
    enabled_flags_for_env,
    invert_unique_aliases,
    merge_tenant_flags,
)


def test_merge_tenant_flags_is_non_mutating() -> None:
    defaults = {"dark_mode": False, "audit_v2": True}
    overrides = {"dark_mode": True, "beta_ai": True}
    merged = merge_tenant_flags(defaults, overrides)
    assert merged == {"dark_mode": True, "audit_v2": True, "beta_ai": True}
    assert defaults == {"dark_mode": False, "audit_v2": True}


def test_enabled_flags_for_env_handles_missing_keys() -> None:
    flags = {
        "new_checkout": {"enabled": True, "envs": ["prod", "staging"]},
        "legacy_ui": {"enabled": False, "envs": ["prod"]},
        "broken": {},
    }
    assert enabled_flags_for_env(flags, "prod") == {"new_checkout": True}


def test_invert_unique_aliases_rejects_collisions() -> None:
    assert invert_unique_aliases({"pay": "svc-payments", "auth": "svc-auth"}) == {
        "svc-payments": "pay",
        "svc-auth": "auth",
    }
    with pytest.raises(ValueError):
        invert_unique_aliases({"pay": "svc-1", "billing": "svc-1"})


def test_diff_flag_snapshots_detects_added_removed_and_changed() -> None:
    before = {"a_unchanged": True, "b_toggled": False, "c_removed": True}
    after = {"a_unchanged": True, "b_toggled": True, "d_added": False}
    diff = diff_flag_snapshots(before, after)
    assert list(diff.keys()) == ["b_toggled", "c_removed", "d_added"]
    assert diff == {
        "b_toggled": (False, True),
        "c_removed": (True, None),
        "d_added": (None, False),
    }
