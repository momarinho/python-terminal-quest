## Concept: SQLAlchemy 2.0 `DeclarativeBase`, Unit of Work & DTO Boundaries

Modern SQLAlchemy 2.0 replaces legacy `Column(...)` and `session.query(...)` with type-checked `DeclarativeBase`, `Mapped[...]`, `mapped_column(...)`, and `select(...)` + `session.scalars(...)`.

### Unit of Work & Never Leaking ORM Instances
A `Session` tracks all dirty/new objects in memory (the **Unit of Work** pattern) and flushes them together inside one transaction. Always map ORM instances into **Pydantic v2 DTOs** (`from_attributes=True`) *before* the `with Session(engine) as session:` block closes—otherwise callers accessing lazy relationships outside the session hit `DetachedInstanceError`!

```python
from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship(back_populates="books")

class AuthorDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
```

*(In production PostgreSQL, pair SQLAlchemy 2.0 with `psycopg` + connection pooling `pool_size=10, max_overflow=20`.)*

### Challenge
Complete `models.py` (`Customer`, `Subscription`), `schemas.py` (`SubscriptionDTO`, `CustomerDTO`), and `service.py` (`register_customer_with_subscription`, `get_customer_summary`) so callers receive pure Pydantic DTOs after the `Session` closes.
