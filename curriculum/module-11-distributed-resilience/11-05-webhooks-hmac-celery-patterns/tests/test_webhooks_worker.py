import pytest
from webhook import WebhookSecurityError, WebhookSignatureVerifier, sign_payload
from worker import TaskQueueWorker


def test_webhook_hmac_verification_and_replay_protection() -> None:
    now = 1_700_000_100.0
    secret = b"whsec_super_secret"
    verifier = WebhookSignatureVerifier(secret, max_age_seconds=120, clock=lambda: now)

    raw_body = b'{"event":"payment.succeeded","amount":4900}'
    sig = sign_payload(secret, 1_700_000_050, raw_body)

    parsed = verifier.verify_and_parse("1700000050", sig, raw_body)
    assert parsed["event"] == "payment.succeeded"
    assert parsed["amount"] == 4900

    # Tampered body fails constant-time digest check
    with pytest.raises(WebhookSecurityError):
        verifier.verify_and_parse("1700000050", sig, b'{"event":"payment.succeeded","amount":999999}')

    # Expired timestamp outside replay window fails
    with pytest.raises(WebhookSecurityError):
        verifier.verify_and_parse("1699999000", sign_payload(secret, 1_699_999_000, raw_body), raw_body)


def test_celery_style_worker_retries_acks_late_and_tracks_states() -> None:
    calls = 0

    def flaky_job(payload: dict[str, object]) -> str:
        nonlocal calls
        calls += 1
        if payload.get("always_fail"):
            raise RuntimeError("hard crash")
        if calls < 3:
            raise ConnectionError("redis temporary hiccup")
        return f"done-{payload['job']}"

    worker = TaskQueueWorker(flaky_job, max_retries=2, acks_late=True, base_delay=0.5, max_delay=4.0)
    worker.enqueue("t-1", {"job": "email"})
    assert worker.results_backend["t-1"].state == "PENDING"

    assert worker.run_next().state == "RETRY"
    assert worker.run_next().state == "RETRY"
    done = worker.run_next()
    assert done is not None
    assert done.state == "SUCCESS"
    assert done.result == "done-email"
    assert done.retry_delays == [0.5, 1.0]
    assert len(worker.broker_queue) == 0

    # Exhausted retries move to FAILURE
    worker.enqueue("t-bad", {"always_fail": True})
    for _ in range(3):
        res = worker.run_next()
    assert res is not None
    assert res.state == "FAILURE"
    assert res.attempts == 3
