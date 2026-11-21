import sys
from typing import TextIO


def format_slo_row(service: str, requests: int, errors: int) -> str:
    """Format one aligned SLO row: '<service:<16> | <requests:>7,> | <errors:>5,> | <success:>6.2%>'."""
    if requests < 0 or errors < 0 or errors > requests:
        raise ValueError("Invalid request/error counts")
    success_rate = 1.0 if requests == 0 else (requests - errors) / requests
    return f"{service:<16} | {requests:>7,} | {errors:>5,} | {success_rate:6.2%}"


def emit_slo_report(
    stdin_stream: TextIO | None = None,
    stdout_stream: TextIO | None = None,
) -> int:
    """Read 'service,requests,errors' lines from stdin_stream and write formatted rows to stdout_stream."""
    in_s = stdin_stream if stdin_stream is not None else sys.stdin
    out_s = stdout_stream if stdout_stream is not None else sys.stdout
    count = 0
    for raw_line in in_s:
        line = raw_line.strip()
        if not line:
            continue
        service_str, req_str, err_str = [part.strip() for part in line.split(",", maxsplit=2)]
        row = format_slo_row(service_str, int(req_str), int(err_str))
        out_s.write(f"{row}\n")
        count += 1
    return count
