import asyncio
from collections.abc import Awaitable


async def with_timeout(coro: Awaitable[str], timeout_sec: float) -> str:
    """Await coro with timeout_sec, returning 'TIMEOUT' if it expires."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout_sec)
    except TimeoutError:
        return "TIMEOUT"
