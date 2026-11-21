import pytest
from queue_buffers import BoundedEventQueue, is_balanced_expression


def test_is_balanced_expression() -> None:
    assert is_balanced_expression("rate_limit(rules=[{a: 1}, (2)])") is True
    assert is_balanced_expression("([)]") is False
    assert is_balanced_expression("(((") is False
    assert is_balanced_expression("]") is False


def test_bounded_event_queue_evicts_and_pops_fifo() -> None:
    q = BoundedEventQueue(maxlen=3)
    q.push("e1")
    q.push("e2")
    q.push("e3")
    q.push("e4")
    assert q.snapshot() == ["e2", "e3", "e4"]
    assert q.pop_oldest() == "e2"
    assert q.pop_oldest() == "e3"
    assert q.pop_oldest() == "e4"
    assert q.pop_oldest() is None

    with pytest.raises(ValueError):
        BoundedEventQueue(0)
