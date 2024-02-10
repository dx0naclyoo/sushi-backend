from pydantic import BaseModel


class BaseCategories(BaseModel):
    name: str


class Categories(BaseCategories):
    id: int


class UpdateCategories(BaseCategories):
    pass


class CreateCategories(BaseCategories):
    pass
