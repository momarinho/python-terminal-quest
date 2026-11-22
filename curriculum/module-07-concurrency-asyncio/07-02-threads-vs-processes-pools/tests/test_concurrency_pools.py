import time

from concurrency_pools import (
    ThreadSafeCounter,
    hash_payloads_parallel,
    run_io_batch,
    run_io_batch_resilient,
    sha256_hex,
)


def test_thread_safe_counter_and_io_pool_order() -> None:
    counter = ThreadSafeCounter()

    def bump(idx: int) -> int:
        time.sleep(0.01)
        counter.increment()
        return idx * 10

    tasks = [lambda i=i: bump(i) for i in range(20)]
    results = run_io_batch(tasks, max_workers=8)
    assert results == [i * 10 for i in range(20)]
    assert counter.value == 20
    assert counter.reset() == 20
    assert counter.value == 0


def test_run_io_batch_resilient_isolates_failures() -> None:
    def ok(val: str) -> str:
        return val

    def boom() -> str:
        raise RuntimeError("upstream timeout")

    results, errors = run_io_batch_resilient(
        [lambda: ok("a"), boom, lambda: ok("b"), boom],
        fallback="N/A",
        max_workers=3,
    )
    assert results == ["a", "N/A", "b", "N/A"]
    assert errors == 2
    assert run_io_batch_resilient([], fallback="N/A") == ([], 0)


def test_hash_payloads_parallel_uses_process_pool() -> None:
    inputs = ["alpha", "beta", "gamma", "delta"]
    digests = hash_payloads_parallel(inputs, max_workers=2)
    assert digests == [sha256_hex(item) for item in inputs]
    assert hash_payloads_parallel([]) == []
