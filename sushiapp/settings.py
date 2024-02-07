import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # database setting
    echo: bool = True

    # app settings
    host: str = "127.0.0.1"
    port: int = 8000

    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings()
