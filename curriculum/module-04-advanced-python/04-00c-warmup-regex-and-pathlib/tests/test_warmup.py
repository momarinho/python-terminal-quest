from pathlib import Path

from warmup import extract_ticket_id, save_text_file


def test_extract_ticket_id() -> None:
    assert extract_ticket_id("Escalated TKT-409 to oncall") == "TKT-409"
    assert extract_ticket_id("No ticket") is None


def test_save_text_file(tmp_path: Path) -> None:
    file_path = tmp_path / "note.txt"
    save_text_file(file_path, "hello pathlib")
    assert file_path.read_text(encoding="utf-8") == "hello pathlib"
