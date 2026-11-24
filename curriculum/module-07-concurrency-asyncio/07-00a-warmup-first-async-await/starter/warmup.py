import asyncio  # noqa: F401


async def double_async(x: int) -> int:
    """Yield control briefly with asyncio.sleep(0) and return x * 2."""
    return 0


def run_double(x: int) -> int:
    """Execute double_async(x) from synchronous Python."""
    return 0
