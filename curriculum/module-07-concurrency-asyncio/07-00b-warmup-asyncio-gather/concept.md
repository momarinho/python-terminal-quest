## Beginner Warm-Up 2: `asyncio.gather` Concurrency

Running coroutines one-by-one in a loop takes `N * delay`. Running them together with `asyncio.gather` runs them concurrently and preserves input order:

```python
import asyncio

async def fetch_tag(name: str) -> str:
    await asyncio.sleep(0)
    return name.upper()

async def fetch_all_tags(names: list[str]) -> list[str]:
    return list(await asyncio.gather(*(fetch_tag(n) for n in names)))
```

### Challenge
Implement `fetch_tag` and `fetch_all_tags` in `warmup.py`.
