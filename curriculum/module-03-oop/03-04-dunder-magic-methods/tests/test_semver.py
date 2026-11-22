import pytest
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


def test_semver_parse_and_bump() -> None:
    parsed = SemVer.parse(" v2.4.9 ")
    assert parsed == SemVer(2, 4, 9)
    assert parsed.bump("patch") == SemVer(2, 4, 10)
    assert parsed.bump("minor") == SemVer(2, 5, 0)
    assert parsed.bump("major") == SemVer(3, 0, 0)

    for bad in ("1.2", "1.2.a", "1.-2.0", "1.2.3.4", ""):
        with pytest.raises(ValueError):
            SemVer.parse(bad)

    with pytest.raises(ValueError):
        parsed.bump("hotfix")


def test_release_queue_len_contains_and_sorted_iter() -> None:
    q = ReleaseQueue()
    q.add(SemVer(2, 0, 0))
    q.add(SemVer(1, 2, 1))
    q.add(SemVer(1, 2, 1))
    q.add(SemVer(1, 10, 0))
    assert len(q) == 3
    assert SemVer(1, 2, 1) in q
    assert SemVer(9, 0, 0) not in q
    assert ("1.2.1" in q) is False
    assert [str(v) for v in q] == ["1.2.1", "1.10.0", "2.0.0"]
