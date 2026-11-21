import time
import uuid

from errors import REQUEST_ID_CTX
from fastapi import FastAPI


def install_request_context_middleware(
    app: FastAPI,
    audit_sink: list[dict[str, object]],
) -> None:
    # TODO: propagate/generate X-Request-ID, bind REQUEST_ID_CTX, echo header, log JSON event, reset in finally
    _ = (app, audit_sink, REQUEST_ID_CTX, time, uuid)
