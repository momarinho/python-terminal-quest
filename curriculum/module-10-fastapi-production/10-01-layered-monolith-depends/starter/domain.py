from typing import Protocol

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    priority: int = Field(default=3, ge=1, le=5)


class TicketOut(BaseModel):
    id: str
    title: str
    priority: int


class TicketRepoPort(Protocol):
    def save(self, ticket: TicketOut) -> None: ...
    def get(self, ticket_id: str) -> TicketOut | None: ...


class InMemoryTicketRepo:
    def __init__(self) -> None:
        self._items: dict[str, TicketOut] = {}

    def save(self, ticket: TicketOut) -> None:
        self._items[ticket.id] = ticket

    def get(self, ticket_id: str) -> TicketOut | None:
        return self._items.get(ticket_id)
