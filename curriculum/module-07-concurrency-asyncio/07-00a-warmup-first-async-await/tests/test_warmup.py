import asyncio

from warmup import double_async, run_double


def test_double_async() -> None:
    assert asyncio.run(double_async(7)) == 14


def test_run_double() -> None:
    assert run_double(9) == 18
