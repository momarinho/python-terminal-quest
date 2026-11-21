from collections.abc import Iterable, Iterator


def iter_non_empty_events(lines: Iterable[str]) -> Iterator[str]:
    """Lazily yield stripped non-blank, non-comment ('#') lines."""
    # TODO: yield lazily (never build a full list)
    if False:
        yield ""


def iter_error_records(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Lazily parse 'LEVEL:message' lines from iter_non_empty_events and yield ERROR records."""
    # TODO: yield {'level': 'ERROR', 'message': msg.strip()} lazily
    if False:
        yield {}


def batch_records[T](records: Iterable[T], size: int) -> Iterator[list[T]]:
    """Lazily yield lists of up to `size` records; raise ValueError immediately if size < 1."""
    # TODO: validate size >= 1 eagerly and yield batches lazily
    if False:
        yield []
