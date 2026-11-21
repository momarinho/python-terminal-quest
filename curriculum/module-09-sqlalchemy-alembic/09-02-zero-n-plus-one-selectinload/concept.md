## Concept: Eliminating N+1 Queries (`joinedload` & `selectinload`)

By default, SQLAlchemy relationships lazy-load on attribute access. Fetching 25 parent rows and iterating `parent.children` fires **1 + 25 = 26 SQL queries**!

### Choosing `joinedload` vs. `selectinload`
* **`joinedload(Parent.to_one)`:** Joins a `N:1` or `1:1` parent in the **same** `SELECT` (1 query total, zero row explosion).
* **`selectinload(Parent.to_many)`:** Fires **one** `SELECT ... WHERE parent_id IN (...)` batch query for all child collections—keeping total queries constant ($O(1)$ queries regardless of $N$ rows!).

```python
stmt = (
    select(Playlist)
    .options(joinedload(Playlist.creator), selectinload(Playlist.tracks))
    .order_by(Playlist.id)
    .limit(20)
)
playlists = session.scalars(stmt).all()
```

### Challenge
Fix `fetch_orders_summary(session, limit=25)` in `repository.py` using `joinedload` + `selectinload` so loading 25 orders with their buyers and line items executes in **`<= 2` SQL queries**!
