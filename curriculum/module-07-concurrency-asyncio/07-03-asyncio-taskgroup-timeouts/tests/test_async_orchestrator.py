import asyncio

import pytest
from async_orchestrator import run_resilient_batch, run_strict_taskgroup


def test_run_strict_taskgroup_runs_concurrently_and_times_out() -> None:
    async def fast(n: int) -> int:
        await asyncio.sleep(0.02)
        return n * 2

    res = asyncio.run(run_strict_taskgroup([lambda i=i: fast(i) for i in range(4)], 1.0))
    assert res == [0, 2, 4, 6]

    async def slow() -> int:
        await asyncio.sleep(0.5)
        return 1

    with pytest.raises(TimeoutError):
        asyncio.run(run_strict_taskgroup([slow], 0.03))


def test_run_resilient_batch_isolates_timeouts_and_exceptions() -> None:
    async def ok_task() -> str:
        await asyncio.sleep(0.01)
        return "ready"

    async def slow_task() -> str:
        await asyncio.sleep(0.5)
        return "late"

    async def bad_task() -> str:
        raise RuntimeError("boom")

    out = asyncio.run(run_resilient_batch([ok_task, slow_task, bad_task], per_task_timeout=0.04))
    assert out == [
        {"ok": "ready", "error": None},
        {"ok": None, "error": "timeout"},
        {"ok": None, "error": "boom"},
    ]
