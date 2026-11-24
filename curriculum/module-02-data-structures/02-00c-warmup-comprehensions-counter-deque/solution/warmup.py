from collections import Counter, deque


def double_positives(nums: list[int]) -> list[int]:
    """Return doubled values for integers strictly greater than 0."""
    return [n * 2 for n in nums if n > 0]


def most_common_word(words: list[str]) -> str:
    """Return the most frequent word from a non-empty word list."""
    return Counter(words).most_common(1)[0][0]


def keep_recent(events: list[str], limit: int) -> list[str]:
    """Keep only the most recent `limit` events using deque(maxlen=...)."""
    return list(deque(events, maxlen=limit))
