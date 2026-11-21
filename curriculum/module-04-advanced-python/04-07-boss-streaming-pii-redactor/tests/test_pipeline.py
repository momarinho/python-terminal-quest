import json
from collections.abc import Iterator
from itertools import islice
from pathlib import Path

from patterns import redact_line
from pipeline import iter_redacted_lines, redact_log_file


def test_redact_line_masks_email_cpf_and_bearer() -> None:
    raw = "user=ana.silva@acme.com cpf=123.456.789-01 auth=Bearer eyJ.abc.def\n"
    sanitized, counts = redact_line(raw)
    assert sanitized == "user=a***@acme.com cpf=***.456.789-** auth=Bearer [REDACTED]\n"
    assert counts == {"emails": 1, "cpfs": 1, "bearers": 1}


def test_iter_redacted_lines_is_lazy_and_streams_files(tmp_path: Path) -> None:
    def infinite() -> Iterator[str]:
        while True:
            yield "email=bob@dev.io\n"

    stream = iter_redacted_lines(infinite())
    assert isinstance(stream, Iterator)
    assert [line for line, _ in islice(stream, 2)] == ["email=b***@dev.io\n", "email=b***@dev.io\n"]

    src = tmp_path / "prod.log"
    dest = tmp_path / "out" / "clean.log"
    stats_dest = tmp_path / "out" / "stats.json"
    src.write_text(
        "INFO ok\n"
        "WARN user=maria@corp.org cpf=999.888.777-66\n"
        "ERR auth=Bearer tok123 email=z@x.co\n",
        encoding="utf-8",
    )

    stats = redact_log_file(src, dest, stats_dest)
    assert stats == {"lines": 3, "emails": 2, "cpfs": 1, "bearers": 1}
    assert "999.888" not in dest.read_text(encoding="utf-8")
    assert "***.888.777-**" in dest.read_text(encoding="utf-8")
    assert json.loads(stats_dest.read_text(encoding="utf-8")) == stats
