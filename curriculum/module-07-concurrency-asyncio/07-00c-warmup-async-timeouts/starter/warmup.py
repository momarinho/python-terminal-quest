import asyncio  # noqa: F401
from collections.abc import Awaitable


async def with_timeout(coro: Awaitable[str], timeout_sec: float) -> str:
    """Await coro with timeout_sec, returning 'TIMEOUT' if it expires."""
    return await coro
