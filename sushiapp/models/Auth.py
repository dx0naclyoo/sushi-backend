from datetime import datetime
from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    registration_data: datetime


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class CreateUser(BaseUser):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
