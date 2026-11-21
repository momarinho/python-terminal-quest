import io

import pytest
from slo_report import emit_slo_report, format_slo_row


def test_format_slo_row_alignment_and_percentages() -> None:
    row = format_slo_row("auth-api", 12500, 25)
    assert row == "auth-api         |  12,500 |    25 | 99.80%"
    assert format_slo_row("idle-svc", 0, 0) == "idle-svc         |       0 |     0 | 100.00%"


def test_emit_slo_report_streams_cleanly() -> None:
    in_buf = io.StringIO("\ncheckout,1000,15\npayments,2000,0\n\n")
    out_buf = io.StringIO()
    count = emit_slo_report(in_buf, out_buf)
    assert count == 2
    lines = out_buf.getvalue().splitlines()
    assert lines == [
        "checkout         |   1,000 |    15 | 98.50%",
        "payments         |   2,000 |     0 | 100.00%",
    ]


def test_rejects_invalid_counts() -> None:
    with pytest.raises(ValueError):
        format_slo_row("api", 10, 11)
