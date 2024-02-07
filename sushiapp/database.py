import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sushiapp.settings import settings

load_dotenv()

# load .env for database
USER_PASSWORD = os.getenv("USER_PASSWORD")
USER_NAME = os.getenv("USER_NAME")
DB_NAME = os.getenv("DB_NAME")
PORT = os.getenv("DB_PORT")
HOST = os.getenv("DB_HOST")

DATABASE_URL = f"postgresql+asyncpg://{USER_NAME}:{USER_PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


class DatabaseWorker:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url, echo=echo)
        self.session_factory = async_sessionmaker(bind=self.engine,
                                                  autoflush=False,
                                                  autocommit=False,
                                                  expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


databaseworker = DatabaseWorker(url=DATABASE_URL, echo=settings.echo)
