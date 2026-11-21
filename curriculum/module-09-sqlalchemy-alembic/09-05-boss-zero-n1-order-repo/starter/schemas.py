from pydantic import BaseModel, ConfigDict


class OrderLineDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sku: str
    qty: int


class OrderDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_email: str
    status: str
    lines: list[OrderLineDTO] = []
