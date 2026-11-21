from domain import TicketCreate, TicketOut, TicketRepoPort


class TicketService:
    def __init__(self, repo: TicketRepoPort) -> None:
        self.repo = repo
        self._seq = 0

    def create_ticket(self, payload: TicketCreate) -> TicketOut:
        # TODO: generate 'tkt-<n>', strip title, save via self.repo, return TicketOut
        _ = payload
        return TicketOut(id="", title="", priority=1)

    def get_ticket(self, ticket_id: str) -> TicketOut | None:
        # TODO: fetch from self.repo
        return None
