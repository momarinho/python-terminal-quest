from warmup import sha256_hex, sign_hmac, verify_hmac


def test_sha256_hex() -> None:
    digest = sha256_hex("order:42")
    assert len(digest) == 64
    assert digest == sha256_hex("order:42")


def test_sign_and_verify_hmac() -> None:
    sig = sign_hmac("top-secret", '{"event":"paid"}')
    assert verify_hmac("top-secret", '{"event":"paid"}', sig) is True
    assert verify_hmac("top-secret", '{"event":"tampered"}', sig) is False
