from typing import Optional

from pydantic import BaseModel


class BaseProduct(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    weight: float


class Product(BaseProduct):
    id: int


class UpdateProduct(BaseProduct):
    pass


class CreateProduct(BaseProduct):
    pass
