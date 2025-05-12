from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Wallet(Base):
    address: Mapped[str] = mapped_column(String)
    private_key: Mapped[str] = mapped_column(String)
