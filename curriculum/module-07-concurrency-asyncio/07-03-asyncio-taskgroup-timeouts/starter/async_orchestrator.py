import asyncio
from collections.abc import Awaitable, Callable


async def run_strict_taskgroup[T](
    task_fns: list[Callable[[], Awaitable[T]]],
    overall_timeout: float,
) -> list[T]:
    """Run all async callables under asyncio.timeout + asyncio.TaskGroup, preserving order."""
    # TODO: use asyncio.timeout(overall_timeout) and asyncio.TaskGroup()
    _ = (asyncio, task_fns, overall_timeout)
    return []


async def run_resilient_batch[T](
    task_fns: list[Callable[[], Awaitable[T]]],
    per_task_timeout: float,
) -> list[dict[str, T | str | None]]:
    """Run all tasks concurrently with per-task timeout, capturing errors without aborting siblings."""
    # TODO: return [{'ok': val, 'error': None}] or [{'ok': None, 'error': 'timeout'|str(exc)}]
    _ = per_task_timeout
    return []
