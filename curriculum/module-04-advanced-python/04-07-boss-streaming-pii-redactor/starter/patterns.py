import re


def redact_line(line: str) -> tuple[str, dict[str, int]]:
    """Redact emails, formatted CPFs (***.XXX.YYY-**), and Bearer tokens; return (redacted, counts)."""
    # TODO: implement compiled regex patterns for emails, cpfs, and bearers
    _ = re
    return line, {"emails": 0, "cpfs": 0, "bearers": 0}
