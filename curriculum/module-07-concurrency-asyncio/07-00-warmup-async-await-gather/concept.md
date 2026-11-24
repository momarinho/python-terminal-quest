## Concept: Warm-Up & Quick Syntax Reveal (Module 7)

Before profiling CPython or coordinating `asyncio.TaskGroup`, make sure `async def`, `await`, `asyncio.gather`, and `asyncio.run` feel natural!

### Pattern Reveal #1 — Defining an `async` Coroutine
```python
import asyncio

async def fetch_value(x: int) -> int:
    await asyncio.sleep(0)
    return x * 2
```

### Pattern Reveal #2 — Running Coroutines Concurrently (`asyncio.gather`)
```python
async def fetch_all(items: list[int]) -> list[int]:
    return list(await asyncio.gather(*(fetch_value(x) for x in items)))
```

### Pattern Reveal #3 — Entry Point from Sync Code (`asyncio.run`)
```python
def run_sync(items: list[int]) -> list[int]:
    return asyncio.run(fetch_all(items))
```

### Challenge
Open `warmup.py` and complete `fetch_value`, `fetch_all`, and `run_sync`.
