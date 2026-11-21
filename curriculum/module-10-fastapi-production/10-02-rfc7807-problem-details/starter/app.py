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
        # TODO: raise ConflictError if duplicate order_id, else store and return
        _ = (ConflictError, orders)
        return {"order_id": body.order_id, "amount_cents": body.amount_cents}

    @app.get("/orders/{order_id}")
    def get_order(order_id: str) -> dict[str, object]:
        # TODO: raise ForbiddenError if order_id == 'secret', NotFoundError if missing, else return
        _ = (ForbiddenError, NotFoundError)
        return {}

    return app
