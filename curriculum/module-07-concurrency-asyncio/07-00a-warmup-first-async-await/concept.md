## Beginner Warm-Up 1: `async def`, `await` & `asyncio.run`

An `async def` function defines a coroutine that yields control when it hits `await`:

```python
import asyncio

async def double_async(x: int) -> int:
    await asyncio.sleep(0)
    return x * 2

def run_double(x: int) -> int:
    return asyncio.run(double_async(x))
```

### Challenge
Complete `double_async` and `run_double` in `warmup.py`.
