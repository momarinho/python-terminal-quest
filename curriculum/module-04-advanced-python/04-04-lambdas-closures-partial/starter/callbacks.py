from collections.abc import Callable
from functools import partial


def build_threshold_checks(thresholds: list[int]) -> list[Callable[[int], bool]]:
    """Return one predicate per threshold returning True iff value >= threshold."""
    # BUG: late binding causes every lambda to use the last threshold!
    checks: list[Callable[[int], bool]] = []
    for t in thresholds:
        checks.append(lambda val: val >= t)  # noqa: B023
    return checks


def make_moving_counter(start: int = 0) -> Callable[[int], int]:
    """Return a stateful counter closure `inc(delta=1) -> new_total`."""
    count = start

    def inc(delta: int = 1) -> int:
        # TODO: use nonlocal count and update by delta
        return count

    return inc


def _format_alert(service: str, env: str, message: str) -> str:
    return f"[{env}] {service}: {message}"


def bind_alert_formatter(service: str, env: str) -> Callable[[str], str]:
    """Use functools.partial to pre-bind `service` and `env` on `_format_alert`."""
    # TODO: return partial(...)
    _ = partial
    return lambda msg: msg
