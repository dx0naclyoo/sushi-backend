import os
from asyncio import current_task

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from sushiapp.settings import settings

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
        self.session_factory = async_sessionmaker(bind=self.engine,
                                                  autoflush=False,
                                                  autocommit=False,
                                                  expire_on_commit=False)

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    # Don't use this function, better use "session_scoped_dependency"
    # async def session_dependency(self) -> AsyncSession:
    #     async with self.session_factory() as session:
    #         yield session
    #         await session.close()

    async def session_scoped_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


databaseworker = DatabaseWorker(url=DATABASE_URL, echo=settings.echo)
