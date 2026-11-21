## Boss Fight: Extensible Order Book Domain

Trading and matching engines depend on strict domain invariants, deterministic ordering, and pluggable execution policies.

### Multi-File Architecture (`models.py` + `strategies.py` + `book.py`)
1. **`models.py`**:
   * `@dataclass(frozen=True) class Order`: `order_id: str`, `side: Literal["BUY", "SELL"]`, `price: Decimal`, `qty: int`, `seq: int = 0`. Validate non-empty `order_id`, `side in {"BUY", "SELL"}`, `price > 0`, `qty > 0`, `seq >= 0` in `__post_init__`.
   * `@dataclass(frozen=True) class TradeFill`: `buy_id: str`, `sell_id: str`, `price: Decimal`, `qty: int`.
2. **`strategies.py`**:
   * `MatchingStrategy(Protocol)`: `match(self, incoming: Order, resting: list[Order]) -> tuple[list[TradeFill], list[Order], Order | None]` returning `(fills, updated_resting, remaining_order_or_none)`.
   * `PriceTimeStrategy`: matches `BUY` against lowest-priced `SELL` (`sell.price <= buy.price`, breaking ties by `seq` asc) and `SELL` against highest-priced `BUY` (`buy.price >= sell.price`, breaking ties by `seq` asc). Execution price is the **resting** order's price! Any unfilled remainder rests on the book.
   * `ImmediateOrCancelStrategy`: uses the same price-time matching priority, but **never** adds an unfilled remainder to the resting book (returns `None` for remainder).
3. **`book.py`**:
   * `OrderBook(strategy: MatchingStrategy | None = None)` (defaults to `PriceTimeStrategy()`):
     * `submit(order: Order) -> list[TradeFill]`: rejects duplicate active `order_id`s with `ValueError`, runs `strategy.match(...)`, updates resting orders, returns fills.
     * `cancel(order_id: str) -> bool`: removes resting order and returns `True`, or `False` if absent.
     * `best_bid() -> Decimal | None` / `best_ask() -> Decimal | None`
     * `__len__() -> int` (resting order count) and `__iter__() -> Iterator[Order]` (yielding resting orders sorted by `seq` ascending).
