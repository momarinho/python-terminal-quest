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

    def push(self, event: str) -> None:
        self._queue.append(event)

    def pop_oldest(self) -> str | None:
        return self._queue.popleft() if self._queue else None

    def snapshot(self) -> list[str]:
        return list(self._queue)
