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
        # BUG: unprotected read-modify-write loses updates under contention!
        self._value += delta
        return self._value

    def reset(self) -> int:
        """Atomically reset the counter to 0 and return its previous value."""
        return 0

    @property
    def value(self) -> int:
        return self._value


def run_io_batch[T](tasks: list[Callable[[], T]], max_workers: int = 4) -> list[T]:
    """Execute zero-arg I/O callables via ThreadPoolExecutor and return results in input order."""
    _ = (ThreadPoolExecutor, max_workers)
    return []


def run_io_batch_resilient[T](
    tasks: list[Callable[[], T]],
    fallback: T,
    max_workers: int = 4,
) -> tuple[list[T], int]:
    """Execute tasks concurrently, substituting `fallback` on task exceptions and returning `(results, error_count)`."""
    return [], 0


def hash_payloads_parallel(payloads: list[str], max_workers: int = 2) -> list[str]:
    """Hash payloads across processes using ProcessPoolExecutor and top-level sha256_hex."""
    _ = (ProcessPoolExecutor, max_workers)
    return []
