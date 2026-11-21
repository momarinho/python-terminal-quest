from functools import partial

from callbacks import (
    bind_alert_formatter,
    build_threshold_checks,
    make_moving_counter,
)


def test_build_threshold_checks_avoids_late_binding_bug() -> None:
    checks = build_threshold_checks([10, 50, 100])
    assert [fn(25) for fn in checks] == [True, False, False]
    assert [fn(100) for fn in checks] == [True, True, True]


def test_make_moving_counter_isolated_closures() -> None:
    c1 = make_moving_counter(10)
    c2 = make_moving_counter(0)
    assert c1(5) == 15
    assert c1(2) == 17
    assert c2(3) == 3


def test_bind_alert_formatter_uses_partial() -> None:
    fmt = bind_alert_formatter("payments", "prod")
    assert isinstance(fmt, partial)
    assert fmt("high latency") == "[prod] payments: high latency"
