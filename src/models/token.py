from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Token(Base):
    address: Mapped[str] = mapped_column(String)
