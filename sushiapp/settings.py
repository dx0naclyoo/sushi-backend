from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database setting
    echo: bool = True

    # app settings
    host: str = "127.0.0.1"
    port: int = 8000


settings = Settings()
