from semver import ReleaseQueue, SemVer


def test_semver_equality_hashing_and_ordering() -> None:
    v1 = SemVer(1, 2, 0)
    v1_dup = SemVer(1, 2, 0)
    v2 = SemVer(1, 10, 0)
    assert v1 == v1_dup
    assert hash(v1) == hash(v1_dup)
    assert v1 < v2
    assert v2 >= v1
    assert repr(v1) == "SemVer(1, 2, 0)"
    assert str(v2) == "1.10.0"
    assert (v1 == "1.2.0") is False


def test_release_queue_len_and_sorted_iter() -> None:
    q = ReleaseQueue()
    q.add(SemVer(2, 0, 0))
    q.add(SemVer(1, 2, 1))
    q.add(SemVer(1, 2, 1))
    q.add(SemVer(1, 10, 0))
    assert len(q) == 3
    assert [str(v) for v in q] == ["1.2.1", "1.10.0", "2.0.0"]
