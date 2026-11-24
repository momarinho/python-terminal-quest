import asyncio


async def fetch_tag(name: str) -> str:
    """Return uppercase tag after awaiting asyncio.sleep(0)."""
    await asyncio.sleep(0)
    return name.upper()


async def fetch_all_tags(names: list[str]) -> list[str]:
    """Fetch all tags concurrently using asyncio.gather."""
    return list(await asyncio.gather(*(fetch_tag(n) for n in names)))
