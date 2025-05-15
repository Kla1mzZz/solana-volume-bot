from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.sqlite import BLOB

import sys
from pathlib import Path


# Add parent directory to Python path to find database module
sys.path.append(str(Path(__file__).parent.parent))

from models.base import Base


class Wallet(Base):    
    address: Mapped[str] = mapped_column(String)
    private_key: Mapped[bytes] = mapped_column(String)
