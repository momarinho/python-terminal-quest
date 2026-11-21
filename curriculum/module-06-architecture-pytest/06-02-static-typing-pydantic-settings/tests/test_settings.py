import pytest
from contracts import build_audit_header
from pydantic import ValidationError
from settings import AppSettings


class FixedClock:
    def now_iso(self) -> str:
        return "2026-01-15T12:00:00Z"


def test_app_settings_loads_env_and_masks_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SVC_SERVICE_NAME", "  orders-api ")
    monkeypatch.setenv("SVC_API_TOKEN", "top-secret-99")
    monkeypatch.setenv("SVC_TIMEOUT_SEC", "2.5")
    monkeypatch.setenv("SVC_MAX_RETRIES", "4")

    cfg = AppSettings()  # type: ignore[call-arg]
    assert cfg.service_name == "orders-api"
    assert cfg.timeout_sec == 2.5
    assert cfg.max_retries == 4
    assert "top-secret-99" not in repr(cfg)

    headers = build_audit_header(cfg, FixedClock())
    assert headers == {
        "X-Service": "orders-api",
        "X-Timestamp": "2026-01-15T12:00:00Z",
        "Authorization": "Bearer top-secret-99",
    }


def test_app_settings_rejects_missing_or_invalid_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SVC_API_TOKEN", raising=False)
    with pytest.raises(ValidationError):
        AppSettings()  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        AppSettings(api_token="ok", timeout_sec=0)  # type: ignore[arg-type]
