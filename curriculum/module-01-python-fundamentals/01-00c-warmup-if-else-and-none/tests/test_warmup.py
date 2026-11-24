from warmup import classify_temp, normalize_retries


def test_classify_temp() -> None:
    assert classify_temp(32) == "HOT"
    assert classify_temp(20) == "WARM"
    assert classify_temp(5) == "COLD"


def test_normalize_retries_preserves_zero() -> None:
    assert normalize_retries(None) == 3
    assert normalize_retries(0) == 0
    assert normalize_retries(5) == 5
