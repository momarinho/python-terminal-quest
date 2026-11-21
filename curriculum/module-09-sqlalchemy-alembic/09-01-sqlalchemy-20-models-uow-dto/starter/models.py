from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    # TODO: add subscriptions relationship(back_populates="customer")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan: Mapped[str] = mapped_column(String(50))
    active: Mapped[bool] = mapped_column(default=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    # TODO: add customer relationship(back_populates="subscriptions")
    _ = relationship
