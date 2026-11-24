import asyncio


async def double_async(x: int) -> int:
    """Yield control briefly with asyncio.sleep(0) and return x * 2."""
    await asyncio.sleep(0)
    return x * 2


def run_double(x: int) -> int:
    """Execute double_async(x) from synchronous Python."""
    return asyncio.run(double_async(x))
