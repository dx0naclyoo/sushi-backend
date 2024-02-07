from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel


class BaseOrder(BaseModel):
    cost: int
    description: Annotated[str, MaxLen(200)]
    data: datetime  # yyyy-MM-DD


class Order(BaseOrder):
    id: int


class OrderCreate(BaseOrder):
    pass


class OrderUpdate(BaseOrder):

    class Config:
        from_attributes = True

# cost: Mapped[float] = mapped_column(sqlalchemy.Float, nullable=False)
# description: Mapped[str] = mapped_column(sqlalchemy.Text)
# data: Mapped[datetime] = mapped_column(
#     DateTime(timezone=True), server_default=func.now())
