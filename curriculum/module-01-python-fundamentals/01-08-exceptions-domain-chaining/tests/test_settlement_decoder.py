import json

import pytest
from settlement_decoder import (
    InvalidAmountError,
    PayloadDecodeError,
    SettlementError,
    decode_settlement,
)


def test_decode_success_runs_else_and_finally() -> None:
    log: list[str] = []
    res = decode_settlement('{"tx_id": " tx_99 ", "amount_cents": 4500}', log)
    assert res == {"tx_id": "tx_99", "amount_cents": 4500}
    assert log == ["OK", "RELEASED"]


def test_malformed_json_chains_cause_and_still_releases() -> None:
    log: list[str] = []
    with pytest.raises(PayloadDecodeError) as exc_info:
        decode_settlement("{broken", log)
    assert isinstance(exc_info.value, SettlementError)
    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)
    assert log == ["RELEASED"]


def test_invalid_amount_raises_domain_error_and_releases() -> None:
    log: list[str] = []
    with pytest.raises(InvalidAmountError):
        decode_settlement('{"tx_id": "tx_1", "amount_cents": -5}', log)
    assert log == ["RELEASED"]
