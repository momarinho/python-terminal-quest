from collections.abc import Iterator
from contextlib import contextmanager
from types import TracebackType

_MISSING = object()


class TransactionScope:
    """Context manager recording BEGIN, then COMMIT on success or ROLLBACK on exception."""

    def __init__(self, audit_log: list[str]) -> None:
        self.audit_log = audit_log

    def __enter__(self) -> "TransactionScope":
        self.audit_log.append("BEGIN")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type is None:
            self.audit_log.append("COMMIT")
        else:
            self.audit_log.append("ROLLBACK")
        return False


@contextmanager
def scoped_env_override(
    env: dict[str, str],
    updates: dict[str, str],
) -> Iterator[dict[str, str]]:
    """Temporarily apply `updates` to `env` and restore exact prior state on exit."""
    previous: dict[str, object] = {key: env.get(key, _MISSING) for key in updates}
    env.update(updates)
    try:
        yield env
    finally:
        for key, old_val in previous.items():
            if old_val is _MISSING:
                env.pop(key, None)
            else:
                env[key] = str(old_val)
