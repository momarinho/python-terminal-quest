## Beginner Warm-Up 3: Async Timeouts (`asyncio.wait_for`)

Production async services always cap how long an I/O call can wait:

```python
import asyncio
from collections.abc import Awaitable

async def with_timeout(coro: Awaitable[str], timeout_sec: float) -> str:
    try:
        return await asyncio.wait_for(coro, timeout=timeout_sec)
    except TimeoutError:
        return "TIMEOUT"
```

### Challenge
Implement `with_timeout` in `warmup.py`.
