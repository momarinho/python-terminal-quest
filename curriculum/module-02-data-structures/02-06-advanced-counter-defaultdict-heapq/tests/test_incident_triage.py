from incident_triage import (
    IncidentPriorityQueue,
    group_alerts_by_service,
    top_error_codes,
)


def test_top_error_codes_breaks_ties_alphabetically() -> None:
    codes = ["E503", "E500", "E503", "E429", "E429", "E404"]
    assert top_error_codes(codes, 2) == [("E429", 2), ("E503", 2)]
    assert top_error_codes(codes, 0) == []


def test_group_alerts_by_service() -> None:
    grouped = group_alerts_by_service([
        ("auth", "token expired"),
        ("pay", "timeout"),
        ("auth", "invalid sig"),
    ])
    assert grouped == {
        "auth": ["token expired", "invalid sig"],
        "pay": ["timeout"],
    }


def test_incident_priority_queue_fifo_tie_break() -> None:
    pq = IncidentPriorityQueue()
    pq.enqueue(2, "inc-low")
    pq.enqueue(1, "inc-p1-first")
    pq.enqueue(1, "inc-p1-second")
    pq.enqueue(0, "inc-p0")

    assert pq.pop_next() == "inc-p0"
    assert pq.pop_next() == "inc-p1-first"
    assert pq.pop_next() == "inc-p1-second"
    assert pq.pop_next() == "inc-low"
    assert pq.pop_next() is None
