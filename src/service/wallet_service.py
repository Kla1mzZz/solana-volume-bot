from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
import asyncio
import base58

from database import get_wallets

client = AsyncClient('https://api.devnet.solana.com')


async def create_wallet(count: int = 1) -> list[tuple[str, str]]:
    wallets = []
    for i in range(count):
        keypair = Keypair()
        pubkey = keypair.pubkey()
        secretkey = keypair.to_bytes()
        wallet = (str(pubkey), base58.b58encode(secretkey).decode())
        wallets.append(wallet)

    return wallets


async def get_balance(secret_key: str) -> int:
    c = base58.b58decode(
        '4sBPJAhFVG67HDZo2Eju3KrciiK9c3GrLC2393bjHeBX29qAf7M18FqpARdd95DrB2rUCYn4nBzpnLNSVd17APQp'
    )

    keypair = Keypair.from_bytes(c)

    balance = await client.get_balance(keypair.pubkey())

    print(balance.value)
    return balance.value


asyncio.run(a())
