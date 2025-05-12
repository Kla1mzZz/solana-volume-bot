from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'

    model_config = SettingsConfigDict(env_nested_delimiter='__')


settings = Settings()
