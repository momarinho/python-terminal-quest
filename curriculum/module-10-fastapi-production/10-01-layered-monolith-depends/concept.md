## Concept: Layered FastAPI Architecture & `Depends(...)` Injection

Keeping SQL, business rules, and HTTP route handlers mixed inside one function makes FastAPI apps hard to test and refactor. Structure each feature as **`api -> service -> domain -> repo`** wired cleanly with `Depends(...)`.

### Clean `Depends` + `app.dependency_overrides`
* Route handlers parse/validate Pydantic request models, call an injected service (`service: BookService = Depends(get_service)`), and return typed response schemas with explicit `status_code` (`201 Created` on creation, `404` when absent).
* Tests swap production repositories for fast in-memory fakes via `app.dependency_overrides[get_repo] = lambda: fake_repo`—zero monkeypatching needed!

```python
from typing import Annotated
from fastapi import Depends, FastAPI, status

def get_catalog_service() -> CatalogService:
    return CatalogService(InMemoryBookRepo())

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(
    body: CreateBookRequest,
    svc: Annotated[CatalogService, Depends(get_catalog_service)],
) -> BookResponse:
    return svc.register(body.isbn, body.title)
```

### Challenge
Implement `TicketCreate`, `TicketOut`, `TicketRepoPort`, `InMemoryTicketRepo` in `domain.py`, `TicketService` in `service.py`, and `create_app` + `APIRouter` (`POST /tickets` `201`, `GET /tickets/{ticket_id}` `200`/`404`) using `Depends` in `app.py`.
