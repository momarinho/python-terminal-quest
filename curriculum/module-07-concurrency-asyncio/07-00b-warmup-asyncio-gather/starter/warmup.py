import asyncio  # noqa: F401


async def fetch_tag(name: str) -> str:
    """Return uppercase tag after awaiting asyncio.sleep(0)."""
    return ""


async def fetch_all_tags(names: list[str]) -> list[str]:
    """Fetch all tags concurrently using asyncio.gather."""
    return []
