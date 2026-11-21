## Boss Fight: Zero-N+1 Order Repository

Combine SQLAlchemy 2.0 `DeclarativeBase` models, Pydantic v2 DTO boundaries, strict zero-N+1 eager loading, and optimistic locking into a production-ready repository.

### Multi-File Architecture (`models.py` + `schemas.py` + `repository.py`)
1. **`models.py`**:
   * `Product`: `sku` (unique `str`), `stock` (`int`), `version` (`int`, `default=1`) with `__mapper_args__ = {"version_id_col": version}`.
   * `Order`: `customer_email` (`str`), `status` (`str`, default `"CONFIRMED"`), `lines` (`relationship(back_populates="order", cascade="all, delete-orphan")`).
   * `OrderLine`: `order_id` (`ForeignKey`), `sku` (`str`), `qty` (`int`).
2. **`schemas.py`**:
   * `OrderLineDTO` (`sku`, `qty`) and `OrderDTO` (`id`, `customer_email`, `status`, `lines: list[OrderLineDTO]`) with `ConfigDict(from_attributes=True)`.
3. **`repository.py`**:
   * `InsufficientStockError(Exception)` and `OrderConflictError(Exception)`.
   * `place_order(session, customer_email: str, items: list[tuple[str, int]]) -> OrderDTO`:
     * Validate non-blank `customer_email`, non-empty `items`, and `qty > 0`.
     * Load requested `Product`s, check `product.stock >= qty` (else raise `InsufficientStockError`), decrement `product.stock -= qty`, create `Order` + `OrderLine`s, `session.flush()` catching `StaleDataError` -> `raise OrderConflictError(...) from exc`, and return `OrderDTO.model_validate(order)`.
   * `list_orders_dto(session, status: str | None = None, limit: int = 50) -> list[OrderDTO]`:
     * Query `Order` with `selectinload(Order.lines)`, optional `status` filter, `order_by(Order.id)`, `limit(limit)` — executing **`<= 2` SQL queries** even for 25+ orders!
