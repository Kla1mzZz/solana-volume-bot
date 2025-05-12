from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings


class DatabaseManager:
    def __init__(
        self,
        url: str,
    ):
        self.engine = create_async_engine(
            url=url
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_factory() as session:
            yield session


db_manager = DatabaseManager(url=settings.database_url)
