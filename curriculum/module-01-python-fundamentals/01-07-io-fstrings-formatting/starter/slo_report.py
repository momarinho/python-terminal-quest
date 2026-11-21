import sys
from typing import TextIO


def format_slo_row(service: str, requests: int, errors: int) -> str:
    """Format one aligned SLO row: '<service:<16> | <requests:>7,> | <errors:>5,> | <success:>6.2%>'."""
    # TODO: compute success rate and format with f-string specifiers
    return f"{service} {requests} {errors}"


def emit_slo_report(
    stdin_stream: TextIO | None = None,
    stdout_stream: TextIO | None = None,
) -> int:
    """Read 'service,requests,errors' lines from stdin_stream and write formatted rows to stdout_stream."""
    in_s = stdin_stream or sys.stdin
    out_s = stdout_stream or sys.stdout
    # TODO: iterate non-empty lines, format each row, write to out_s, return row count
    _ = (in_s, out_s)
    return 0
