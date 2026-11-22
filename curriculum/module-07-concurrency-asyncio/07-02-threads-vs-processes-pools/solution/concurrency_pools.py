import hashlib
import threading
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def sha256_hex(text: str) -> str:
    """Top-level picklable CPU worker function computing SHA-256 hex digest."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ThreadSafeCounter:
    def __init__(self, initial: int = 0) -> None:
        self._value = initial
        self._lock = threading.Lock()

    def increment(self, delta: int = 1) -> int:
        with self._lock:
            self._value += delta
            return self._value

    def reset(self) -> int:
        """Atomically reset the counter to 0 and return its previous value."""
        with self._lock:
            previous = self._value
            self._value = 0
            return previous

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


def run_io_batch[T](tasks: list[Callable[[], T]], max_workers: int = 4) -> list[T]:
    """Execute zero-arg I/O callables via ThreadPoolExecutor and return results in input order."""
    if not tasks:
        return []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(task) for task in tasks]
        return [fut.result() for fut in futures]


def run_io_batch_resilient[T](
    tasks: list[Callable[[], T]],
    fallback: T,
    max_workers: int = 4,
) -> tuple[list[T], int]:
    """Execute tasks concurrently, substituting `fallback` on task exceptions and returning `(results, error_count)`."""
    if not tasks:
        return [], 0
    results: list[T] = []
    errors = 0
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(task) for task in tasks]
        for fut in futures:
            try:
                results.append(fut.result())
            except Exception:
                results.append(fallback)
                errors += 1
    return results, errors


def hash_payloads_parallel(payloads: list[str], max_workers: int = 2) -> list[str]:
    """Hash payloads across processes using ProcessPoolExecutor and top-level sha256_hex."""
    if not payloads:
        return []
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(sha256_hex, payloads))
