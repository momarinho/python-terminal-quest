from domain import TicketCreate, TicketOut, TicketRepoPort


class TicketService:
    def __init__(self, repo: TicketRepoPort) -> None:
        self.repo = repo
        self._seq = 0

    def create_ticket(self, payload: TicketCreate) -> TicketOut:
        self._seq += 1
        ticket = TicketOut(
            id=f"tkt-{self._seq}",
            title=payload.title.strip(),
            priority=payload.priority,
        )
        self.repo.save(ticket)
        return ticket

    def get_ticket(self, ticket_id: str) -> TicketOut | None:
        return self.repo.get(ticket_id)
