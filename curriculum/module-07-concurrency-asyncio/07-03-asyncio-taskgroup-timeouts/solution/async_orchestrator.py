import asyncio
from collections.abc import Awaitable, Callable


async def run_strict_taskgroup[T](
    task_fns: list[Callable[[], Awaitable[T]]],
    overall_timeout: float,
) -> list[T]:
    """Run all async callables under asyncio.timeout + asyncio.TaskGroup, preserving order."""
    if overall_timeout <= 0:
        raise ValueError("overall_timeout must be positive")
    if not task_fns:
        return []

    async with asyncio.timeout(overall_timeout), asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fn()) for fn in task_fns]
    return [task.result() for task in tasks]


async def run_resilient_batch[T](
    task_fns: list[Callable[[], Awaitable[T]]],
    per_task_timeout: float,
) -> list[dict[str, T | str | None]]:
    """Run all tasks concurrently with per-task timeout, capturing errors without aborting siblings."""
    if per_task_timeout <= 0:
        raise ValueError("per_task_timeout must be positive")
    if not task_fns:
        return []

    async def _run_one(fn: Callable[[], Awaitable[T]]) -> dict[str, T | str | None]:
        try:
            async with asyncio.timeout(per_task_timeout):
                val = await fn()
                return {"ok": val, "error": None}
        except TimeoutError:
            return {"ok": None, "error": "timeout"}
        except Exception as exc:
            return {"ok": None, "error": str(exc)}

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_run_one(fn)) for fn in task_fns]
    return [task.result() for task in tasks]
