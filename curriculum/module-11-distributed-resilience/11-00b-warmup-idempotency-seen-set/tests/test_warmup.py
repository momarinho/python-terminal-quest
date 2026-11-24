from warmup import SimpleDeduplicator


def test_first_execution_and_replay() -> None:
    dedup = SimpleDeduplicator()
    assert dedup.process_once("evt-1", "charged") == ("ok:charged", False)
    assert dedup.process_once("evt-1", "charged") == ("ok:charged", True)


def test_distinct_keys_process_independently() -> None:
    dedup = SimpleDeduplicator()
    assert dedup.process_once("evt-1", "a")[1] is False
    assert dedup.process_once("evt-2", "b")[1] is False
