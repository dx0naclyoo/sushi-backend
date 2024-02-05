from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from sushiapp.settings import settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from sqlalchemy import exc

load_dotenv()

# load .env for database
USER_PASSWORD = os.getenv("USER_PASSWORD")
USER_NAME = os.getenv("USER_NAME")
DB_NAME = os.getenv("DB_NAME")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")

DATABASE_URL = f"postgresql+asyncpg://{USER_NAME}:{USER_PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


# It is necessary to create a class to work with the DB | functions in the class need to be created asynchronous

class DatabaseWorker:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url, echo=echo)
        self.session_factory = async_sessionmaker(self.engine, autoflush=False, autocommit=False,
                                                  expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self):

        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.close()


databaseworker = DatabaseWorker(url=DATABASE_URL, echo=settings.echo)
