from pydantic import BaseModel, ConfigDict


class SubscriptionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plan: str
    active: bool


class CustomerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    subscriptions: list[SubscriptionDTO] = []
