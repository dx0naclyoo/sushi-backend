from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrdersBase(BaseModel):
    amount: float
    description: Optional[str]
    data: date


class Order(OrdersBase):
    model_config = ConfigDict(from_attributes=True)
    pass


class OrderCreate(OrdersBase):
    user_id: int

# class Orders(Base):
#     __tablename__ = "orders"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#
#     kind: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
#     amount: Mapped[float] = mapped_column(sqlalchemy.Float, nullable=False)
#     description: Mapped[str] = mapped_column(sqlalchemy.Text)
#     data: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now())
#
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["Users"] = relationship(back_populates="orders")
