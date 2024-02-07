from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class User(BaseUser):
    id: int

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
