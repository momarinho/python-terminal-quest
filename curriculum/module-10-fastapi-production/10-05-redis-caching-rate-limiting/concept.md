# Redis Caching & Sliding-Window Rate Limiting

Low-latency FastAPI APIs protect PostgreSQL with two Redis-backed layers: **cache-aside reads** and **sliding-window rate limiting**.

## 1. Cache-Aside, TTL & Explicit Write Invalidation

1. **Read path (`GET /catalog/{id}`):** Check Redis (`GET key`). On hit -> return cached JSON (`X-Cache: HIT`). On miss -> read DB, write Redis with TTL (`SET key val EX 30`), and return `X-Cache: MISS`.
2. **Write path (`PUT /catalog/{id}`):** Update DB first, then **explicitly invalidate** (`DEL key`) so subsequent reads never serve stale data until TTL expires.
3. **Cache Stampede note:** When hot keys expire simultaneously, jitter TTLs or use a single-flight lock (`SET lock nx ex 5`) so only one worker queries the database.

## 2. Sliding-Window Rate Limiting (`ZREMRANGEBYSCORE` / `ZADD`)

Fixed-minute buckets allow 2x bursts across minute boundaries (`00:59` + `01:00`). A **sliding window** tracks exact event timestamps per client within `[now - window, now]`:
- In production Redis: `ZREMRANGEBYSCORE`, `ZCARD`, `ZADD`, `EXPIRE` inside an atomic Lua script / pipeline.
- When `count >= limit`: reject with **`HTTP 429 Too Many Requests`** and header **`Retry-After: <seconds>`**.

```python
from collections import deque

def prune_window(events: deque[float], now: float, window: float) -> None:
    cutoff = now - window
    while events and events[0] <= cutoff:
        events.popleft()
```
