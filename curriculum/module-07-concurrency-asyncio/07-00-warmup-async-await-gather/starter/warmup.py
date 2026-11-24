import asyncio  # noqa: F401


async def fetch_value(x: int) -> int:
    """Simulate an async I/O hop and return x * 2."""
    # Reveal: await asyncio.sleep(0); return x * 2
    return 0


async def fetch_all(items: list[int]) -> list[int]:
    """Run fetch_value concurrently across all items using asyncio.gather."""
    # Reveal: return list(await asyncio.gather(*(fetch_value(x) for x in items)))
    return []


def run_sync(items: list[int]) -> list[int]:
    """Run the async fetch_all coroutine from synchronous code."""
    # Reveal: return asyncio.run(fetch_all(items))
    return []
