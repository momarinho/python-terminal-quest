from collections.abc import Callable
from functools import partial


def _gte_threshold(limit: int, value: int) -> bool:
    return value >= limit


def build_threshold_checks(thresholds: list[int]) -> list[Callable[[int], bool]]:
    """Return one predicate per threshold returning True iff value >= threshold."""
    return [partial(_gte_threshold, t) for t in thresholds]


def make_moving_counter(start: int = 0) -> Callable[[int], int]:
    """Return a stateful counter closure `inc(delta=1) -> new_total`."""
    count = start

    def inc(delta: int = 1) -> int:
        nonlocal count
        count += delta
        return count

    return inc


def _format_alert(service: str, env: str, message: str) -> str:
    return f"[{env}] {service}: {message}"


def bind_alert_formatter(service: str, env: str) -> Callable[[str], str]:
    """Use functools.partial to pre-bind `service` and `env` on `_format_alert`."""
    return partial(_format_alert, service, env)
