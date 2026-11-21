import pytest
from resource_guard import TransactionScope, scoped_env_override


def test_transaction_scope_commit_and_rollback() -> None:
    log: list[str] = []
    with TransactionScope(log):
        log.append("WORK")
    assert log == ["BEGIN", "WORK", "COMMIT"]

    err_log: list[str] = []
    with pytest.raises(ValueError), TransactionScope(err_log):
        err_log.append("WORK")
        raise ValueError("boom")
    assert err_log == ["BEGIN", "WORK", "ROLLBACK"]


def test_scoped_env_override_restores_deleted_and_modified_keys() -> None:
    env = {"MODE": "prod", "PORT": "8080"}
    with pytest.raises(RuntimeError), scoped_env_override(
        env, {"MODE": "test", "DEBUG": "1"}
    ):
        assert env == {"MODE": "test", "PORT": "8080", "DEBUG": "1"}
        raise RuntimeError("abort")

    assert env == {"MODE": "prod", "PORT": "8080"}
