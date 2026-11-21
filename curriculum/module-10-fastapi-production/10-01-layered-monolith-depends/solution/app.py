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

    @router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
    def create_ticket(
        body: TicketCreate,
        svc: Annotated[TicketService, Depends(get_service)],
    ) -> TicketOut:
        return svc.create_ticket(body)

    @router.get("/{ticket_id}", response_model=TicketOut)
    def read_ticket(
        ticket_id: str,
        svc: Annotated[TicketService, Depends(get_service)],
    ) -> TicketOut:
        found = svc.get_ticket(ticket_id)
        if found is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return found

    app.include_router(router)
    return app
