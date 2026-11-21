from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from cache import CacheStore
from fastapi import Depends, FastAPI, Header, HTTPException, Response
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

    def enforce_rate_limit(x_client_id: str = Header(default="anon")) -> None:
        allowed, retry_after = limiter.allow(x_client_id)
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(retry_after)},
            )

    @app.get("/products/{sku}")
    def get_product(
        sku: str,
        response: Response,
        _: None = Depends(enforce_rate_limit),
    ) -> dict[str, object]:
        cache_key = f"product:{sku}"
        cached = cache.get(cache_key)
        if cached is not None:
            response.headers["X-Cache"] = "HIT"
            return dict(json.loads(cached))

        rec = repo.get_by_sku(sku)
        if rec is None:
            raise HTTPException(status_code=404, detail=f"Product '{sku}' not found")
        payload = asdict(rec)
        cache.set(cache_key, json.dumps(payload), cache_ttl_seconds)
        response.headers["X-Cache"] = "MISS"
        return payload

    @app.put("/products/{sku}")
    def update_product_price(
        sku: str,
        body: PriceUpdate,
        _: None = Depends(enforce_rate_limit),
    ) -> dict[str, object]:
        updated = repo.update_price(sku, body.price_cents)
        if updated is None:
            raise HTTPException(status_code=404, detail=f"Product '{sku}' not found")
        cache.delete(f"product:{sku}")
        return asdict(updated)

    return app
