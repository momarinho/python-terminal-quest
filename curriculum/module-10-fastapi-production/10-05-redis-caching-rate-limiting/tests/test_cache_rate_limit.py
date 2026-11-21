from app import ProductRecord, ProductRepository, create_app
from cache import InMemoryRedisCache
from fastapi.testclient import TestClient
from rate_limiter import SlidingWindowRateLimiter


def test_cache_aside_ttl_expiry_and_write_invalidation() -> None:
    now = 100.0
    repo = ProductRepository({"sku-1": ProductRecord("sku-1", "Mechanical Keyboard", 12900)})
    cache = InMemoryRedisCache(clock=lambda: now)
    limiter = SlidingWindowRateLimiter(limit=20, window_seconds=60.0, clock=lambda: now)
    client = TestClient(create_app(repo, cache, limiter, cache_ttl_seconds=10))

    r1 = client.get("/products/sku-1")
    assert r1.status_code == 200
    assert r1.headers["X-Cache"] == "MISS"
    assert repo.read_count == 1

    r2 = client.get("/products/sku-1")
    assert r2.status_code == 200
    assert r2.headers["X-Cache"] == "HIT"
    assert repo.read_count == 1

    # Write invalidates cache immediately
    u1 = client.put("/products/sku-1", json={"price_cents": 14900})
    assert u1.status_code == 200
    r3 = client.get("/products/sku-1")
    assert r3.headers["X-Cache"] == "MISS"
    assert r3.json()["price_cents"] == 14900
    assert repo.read_count == 2

    # Advance virtual clock past TTL -> expires cleanly
    now += 11.0
    r4 = client.get("/products/sku-1")
    assert r4.headers["X-Cache"] == "MISS"
    assert repo.read_count == 3


def test_sliding_window_rate_limiter_returns_429_and_recovers() -> None:
    now = 50.0
    repo = ProductRepository({"sku-1": ProductRecord("sku-1", "USB Hub", 3900)})
    cache = InMemoryRedisCache(clock=lambda: now)
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=5.0, clock=lambda: now)
    client = TestClient(create_app(repo, cache, limiter))

    assert client.get("/products/sku-1", headers={"X-Client-ID": "c-1"}).status_code == 200
    now += 2.0
    assert client.get("/products/sku-1", headers={"X-Client-ID": "c-1"}).status_code == 200

    blocked = client.get("/products/sku-1", headers={"X-Client-ID": "c-1"})
    assert blocked.status_code == 429
    assert int(blocked.headers["Retry-After"]) >= 1

    # Other client still unaffected
    assert client.get("/products/sku-1", headers={"X-Client-ID": "c-2"}).status_code == 200

    # Window slides past first call (50.0 + 5.0 = 55.0)
    now = 55.5
    assert client.get("/products/sku-1", headers={"X-Client-ID": "c-1"}).status_code == 200
