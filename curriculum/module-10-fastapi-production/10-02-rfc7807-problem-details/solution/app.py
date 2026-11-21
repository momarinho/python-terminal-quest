from errors import ConflictError, ForbiddenError, NotFoundError, register_problem_handlers
from fastapi import FastAPI
from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    order_id: str = Field(min_length=1)
    amount_cents: int = Field(gt=0)


def create_app() -> FastAPI:
    app = FastAPI(title="RFC 7807 Orders")
    register_problem_handlers(app)
    orders: dict[str, dict[str, object]] = {}

    @app.post("/orders", status_code=201)
    def create_order(body: OrderCreate) -> dict[str, object]:
        if body.order_id in orders:
            raise ConflictError(f"Order '{body.order_id}' already exists")
        record: dict[str, object] = {
            "order_id": body.order_id,
            "amount_cents": body.amount_cents,
        }
        orders[body.order_id] = record
        return record

    @app.get("/orders/{order_id}")
    def get_order(order_id: str) -> dict[str, object]:
        if order_id == "secret":
            raise ForbiddenError("Access to restricted order is forbidden")
        found = orders.get(order_id)
        if found is None:
            raise NotFoundError(f"Order '{order_id}' was not found")
        return found

    return app
