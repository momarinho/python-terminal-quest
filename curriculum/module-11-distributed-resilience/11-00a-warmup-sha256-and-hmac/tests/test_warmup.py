from warmup import sha256_hex, sign_hmac, verify_hmac


def test_sha256_hex() -> None:
    d = sha256_hex("event:1")
    assert len(d) == 64 and d == sha256_hex("event:1")


def test_hmac_sign_and_verify() -> None:
    sig = sign_hmac("secret", "payload")
    assert verify_hmac("secret", "payload", sig) is True
    assert verify_hmac("secret", "tampered", sig) is False
