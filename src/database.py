from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from models.wallet import Wallet
from models.base import Base
from config import settings


class DatabaseManager:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url, echo=False)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self):
        await self.engine.dispose()


db_manager = DatabaseManager(url=settings.database_url)


async def add_wallets_to_db(wallets: list[tuple[str, str]]):
    async with db_manager.get_session() as session:
        for wallet in wallets:
            session.add(
                Wallet(
                    address=wallet[0],
                    private_key=wallet[1],
                )
            )
        await session.commit()


async def get_all_wallets():
    async with db_manager.get_session() as session:
        return (await session.execute(select(Wallet))).scalars().all()


async def get_main_wallet():
    async with db_manager.get_session() as session:
        wallet_query = select(Wallet).where(Wallet.id == 1)
        main_wallet = (await session.execute(wallet_query)).scalar_one_or_none()
        return main_wallet


async def get_wallets():
    async with db_manager.get_session() as session:
        stmt = select(Wallet).where(Wallet.id >= 2)
        result = await session.execute(stmt)
        return result.scalars().all()
