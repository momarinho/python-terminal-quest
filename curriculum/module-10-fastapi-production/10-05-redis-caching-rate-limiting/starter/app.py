from __future__ import annotations

from dataclasses import dataclass

from cache import CacheStore
from fastapi import FastAPI
from pydantic import BaseModel, Field
from rate_limiter import SlidingWindowRateLimiter


@dataclass
class ProductRecord:
    sku: str
    name: str
    price_cents: int


class ProductRepository:
    def __init__(self, initial: dict[str, ProductRecord]) -> None:
        self._rows = dict(initial)
        self.read_count = 0

    def get_by_sku(self, sku: str) -> ProductRecord | None:
        self.read_count += 1
        return self._rows.get(sku)

    def update_price(self, sku: str, price_cents: int) -> ProductRecord | None:
        rec = self._rows.get(sku)
        if rec is None:
            return None
        updated = ProductRecord(sku=rec.sku, name=rec.name, price_cents=price_cents)
        self._rows[sku] = updated
        return updated


class PriceUpdate(BaseModel):
    price_cents: int = Field(gt=0)


def create_app(
    repo: ProductRepository,
    cache: CacheStore,
    limiter: SlidingWindowRateLimiter,
    cache_ttl_seconds: int = 30,
) -> FastAPI:
    app = FastAPI(title="Catalog Cache & Rate Limit API")

    # TODO:
    # 1. Enforce limiter.allow(X-Client-ID or 'anon') returning HTTP 429 + Retry-After header when denied
    # 2. Implement GET /products/{sku} with cache-aside ('product:{sku}') + X-Cache: HIT | MISS header
    # 3. Implement PUT /products/{sku} updating repo AND calling cache.delete('product:{sku}')
    return app
