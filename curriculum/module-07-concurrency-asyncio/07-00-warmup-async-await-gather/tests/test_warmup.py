import asyncio

from warmup import fetch_all, fetch_value, run_sync


def test_fetch_value() -> None:
    assert asyncio.run(fetch_value(7)) == 14


def test_fetch_all() -> None:
    assert asyncio.run(fetch_all([1, 3, 5])) == [2, 6, 10]


def test_run_sync() -> None:
    assert run_sync([4, 0, 9]) == [8, 0, 18]
