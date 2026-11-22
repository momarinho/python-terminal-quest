from collections import deque

_PAIRS = {")": "(", "]": "[", "}": "{"}
_OPENERS = set(_PAIRS.values())


def is_balanced_expression(text: str) -> bool:
    """Return True iff (), [], and {} delimiters in `text` are properly nested and closed."""
    stack: list[str] = []
    for ch in text:
        if ch in _OPENERS:
            stack.append(ch)
        elif ch in _PAIRS and (not stack or stack.pop() != _PAIRS[ch]):
            return False
    return len(stack) == 0


class BoundedEventQueue:
    """Fixed-capacity FIFO buffer backed by collections.deque."""

    def __init__(self, maxlen: int) -> None:
        if maxlen < 1:
            raise ValueError(f"maxlen must be >= 1, got {maxlen}")
        self._queue: deque[str] = deque(maxlen=maxlen)
        self._evicted = 0

    @property
    def evicted_count(self) -> int:
        """Total number of oldest events evicted due to capacity overflow."""
        return self._evicted

    def push(self, event: str) -> None:
        """Append event, incrementing evicted_count if the buffer was already at maxlen."""
        if self._queue.maxlen is not None and len(self._queue) == self._queue.maxlen:
            self._evicted += 1
        self._queue.append(event)

    def pop_oldest(self) -> str | None:
        """Remove and return oldest event in O(1), or None if empty."""
        return self._queue.popleft() if self._queue else None

    def drain_matching(self, prefix: str) -> list[str]:
        """Remove and return all queued events starting with `prefix` in FIFO order."""
        drained: list[str] = []
        for _ in range(len(self._queue)):
            item = self._queue.popleft()
            if item.startswith(prefix):
                drained.append(item)
            else:
                self._queue.append(item)
        return drained

    def snapshot(self) -> list[str]:
        return list(self._queue)
