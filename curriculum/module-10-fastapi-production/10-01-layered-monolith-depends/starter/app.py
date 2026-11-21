from typing import Annotated

from domain import InMemoryTicketRepo, TicketCreate, TicketOut, TicketRepoPort
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from service import TicketService

_DEFAULT_REPO = InMemoryTicketRepo()


def get_repo() -> TicketRepoPort:
    return _DEFAULT_REPO


def get_service(repo: Annotated[TicketRepoPort, Depends(get_repo)]) -> TicketService:
    return TicketService(repo)


def create_app() -> FastAPI:
    app = FastAPI(title="Ticket Service")
    router = APIRouter(prefix="/tickets", tags=["tickets"])
    _ = (HTTPException, status, TicketCreate, TicketOut)

    # TODO: wire POST /tickets (201) and GET /tickets/{ticket_id} (200 or 404) using Depends(get_service)
    app.include_router(router)
    return app
