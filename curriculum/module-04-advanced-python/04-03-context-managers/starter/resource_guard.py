from collections.abc import Iterator
from contextlib import contextmanager
from types import TracebackType


class TransactionScope:
    """Context manager recording BEGIN, then COMMIT on success or ROLLBACK on exception."""

    def __init__(self, audit_log: list[str]) -> None:
        self.audit_log = audit_log

    def __enter__(self) -> "TransactionScope":
        # TODO: append 'BEGIN' and return self
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        # TODO: append 'COMMIT' if exc_type is None else 'ROLLBACK', propagate exceptions (False)
        return False


@contextmanager
def scoped_env_override(
    env: dict[str, str],
    updates: dict[str, str],
) -> Iterator[dict[str, str]]:
    """Temporarily apply `updates` to `env` and restore exact prior state on exit."""
    # TODO: save original values/missing keys, update env, yield env, restore in finally
    yield env
