from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from turtle import reset

from base58 import b58decode
from base64 import b64decode
from solders.pubkey import Pubkey
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from models.wallet import Wallet
from models.base import Base
from models.token import Token
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
    
    
async def add_token_to_db(token_address: str):
    async with db_manager.get_session() as session:
        adress_query = select(func.count('*')).where(Token.id == 1)
        adress_matched_count: int = (await session.execute(adress_query)).scalar()
        
        try:
            if adress_matched_count == 0:
                session.add(Token(address=token_address))
                await session.commit()
                return f"Токен {token_address} успешно добавлен в базу данных."
            else:
                stmt = select(Token).where(Token.id == 1)
                result = await session.execute(stmt)
                token = result.scalar_one_or_none()
                token.address = token_address
                await session.commit()
                return f"Токен {token_address} успешно перезаписан."
        except ValueError:
            return 'Неверный адрес токена. Убедитесь, что он в формате base58 и имеет длину 32 байта.'
        
async def get_token_address():
    async with db_manager.get_session() as session:
        stmt = select(Token).where(Token.id == 1)
        result = await session.execute(stmt)
        token = result.scalar_one_or_none()
        if token:
            return token.address
        else:
            return 'Вы не добавили токен в базу данных.'
        
