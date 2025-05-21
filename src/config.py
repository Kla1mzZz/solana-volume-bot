from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    https_rpc_endpoint: str = 'https://solana-rpc.publicnode.com'
    BUY_SLIPPAGE: float = 0.3
    SELL_SLIPPAGE: float = 0.1
    SWAP_PRIORITY_FEE: int = 1500000
    mint: str = 'Dz2dRW6dSFTb7yYXSGrxg1f57KsxeVTLWvom2h3oJJL1'

    model_config = SettingsConfigDict(env_nested_delimiter='__')


settings = Settings()
