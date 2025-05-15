import re
from solders.message import Message
from solders.keypair import Keypair
from solders.hash import Hash
from solders.transaction import Transaction
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
import base58



import sys
from pathlib import Path

import asyncio

# Add parent directory to Python path to find database module
# sys.path.append(str(Path(__file__).parent.parent))

from database import add_wallets_to_db


async def create_wallet(count: int = 1) -> list[tuple[str, str]]:
    wallets = []
    for i in range(count):
        keypair = Keypair()
        pubkey = keypair.pubkey()
        secretkey = keypair.to_bytes()
        wallet = (str(pubkey), base58.b58encode(secretkey).decode())
        wallets.append(wallet)
        
    # await add_wallets_to_db(wallets)
    return wallets



