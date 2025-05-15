# # from typing import AsyncGenerator, Any
# # from contextlib import asynccontextmanager
# # from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, 

# from contextlib import asynccontextmanager
# from collections.abc import AsyncIterator

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from models.wallet import Wallet
# from solders.pubkey import Pubkey

# from config import settings


# class DatabaseManager:
#     def __init__(
#         self,
#         url: str,
#     ):
#         self.engine = create_async_engine(url=url)
#         self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
#             bind=self.engine,
#             autoflush=False,
#             autocommit=False,
#             expire_on_commit=False,
#             class_=AsyncSession,
#         )

#     async def dispose(self):
#         await self.engine.dispose()

#     async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
#         async with self.session_factory() as session:
#             yield session


# db_manager = DatabaseManager(url=settings.database_url)

# engine = create_async_engine(settings.database_url)

# def async_session_generator() -> sessionmaker[AsyncSession]:
#     return sessionmaker[AsyncSession](
#         engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#     )


# @asynccontextmanager
# async def get_session() -> AsyncIterator[AsyncSession]:
#     try:
#         async_session = async_session_generator()

#         async with async_session() as session:
#             yield session
#     except:
#         await session.rollback()
#         raise
#     finally:
#         await session.close()
        
        
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from models.wallet import Wallet
from models.base import Base
from config import settings




class DatabaseManager:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url, echo=True)
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
            session.add(Wallet(
                address=wallet[0],
                private_key=wallet[1],
            ))
        await session.commit()
        
        
async def show_main_wallet():
    async with db_manager.get_session() as session:
        wallet_query = select(func.count('*')).where(Wallet.id == 1)
        main_wallet: str = (await session.execute(wallet_query)).scalar()
        return main_wallet
