from collections.abc import Iterator
from itertools import islice

import pytest
from lazy_pipeline import (
    batch_records,
    iter_error_records,
    iter_non_empty_events,
    take_unique_messages,
)


def test_pipeline_is_truly_lazy_on_infinite_stream() -> None:
    def infinite_logs() -> Iterator[str]:
        idx = 0
        while True:
            idx += 1
            yield f"# comment {idx}"
            yield f"INFO:heartbeat {idx}"
            yield f"ERROR:timeout {idx}"

    stream = iter_error_records(infinite_logs())
    assert isinstance(stream, Iterator)
    first_two = list(islice(stream, 2))
    assert first_two == [
        {"level": "ERROR", "message": "timeout 1"},
        {"level": "ERROR", "message": "timeout 2"},
    ]


def test_iter_non_empty_and_batch_records() -> None:
    lines = ["  ", "# skip", " INFO:ok ", "ERROR:disk full", "ERROR:oom", "ERROR:bad"]
    assert list(iter_non_empty_events(lines)) == [
        "INFO:ok",
        "ERROR:disk full",
        "ERROR:oom",
        "ERROR:bad",
    ]
    batches = list(batch_records(iter_error_records(lines), 2))
    assert batches == [
        [{"level": "ERROR", "message": "disk full"}, {"level": "ERROR", "message": "oom"}],
        [{"level": "ERROR", "message": "bad"}],
    ]
    with pytest.raises(ValueError):
        batch_records([], 0)


def test_take_unique_messages_stops_early_on_infinite_stream() -> None:
    pulls = 0

    def repeating_infinite_records() -> Iterator[dict[str, str]]:
        nonlocal pulls
        items = [
            {"level": "ERROR", "message": "timeout"},
            {"level": "ERROR", "message": "timeout"},
            {"level": "ERROR", "message": "oom"},
            {"level": "ERROR", "message": "disk"},
        ]
        while True:
            for item in items:
                pulls += 1
                yield item

    assert list(take_unique_messages(repeating_infinite_records(), 0)) == []
    assert pulls == 0

    unique_two = list(take_unique_messages(repeating_infinite_records(), 2))
    assert unique_two == [
        {"level": "ERROR", "message": "timeout"},
        {"level": "ERROR", "message": "oom"},
    ]
    assert pulls == 3

    with pytest.raises(ValueError):
        take_unique_messages([], -1)
