import asyncio

from warmup import with_timeout


async def _fast() -> str:
    await asyncio.sleep(0)
    return "OK"


async def _slow() -> str:
    await asyncio.sleep(0.5)
    return "LATE"


def test_with_timeout_fast() -> None:
    assert asyncio.run(with_timeout(_fast(), 0.2)) == "OK"


def test_with_timeout_slow() -> None:
    assert asyncio.run(with_timeout(_slow(), 0.01)) == "TIMEOUT"
