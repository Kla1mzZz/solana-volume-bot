import base58
import asyncio

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
import asyncio
import base58


async def create_wallet(count: int = 1) -> list[tuple[str, str]]:
    wallets = []
    for i in range(count):
        keypair = Keypair()
        pubkey = keypair.pubkey()
        secretkey = keypair.to_bytes()
        wallet = (str(pubkey), base58.b58encode(secretkey).decode())
        wallets.append(wallet)

    return wallets

async def a():
    client = AsyncClient('https://api.devnet.solana.com')
    
    c = base58.b58decode('4sBPJAhFVG67HDZo2Eju3KrciiK9c3GrLC2393bjHeBX29qAf7M18FqpARdd95DrB2rUCYn4nBzpnLNSVd17APQp')
    
    k = Keypair.from_bytes(c)
    
    b = await client.get_balance(k.pubkey())
    
    print(b)

asyncio.run(a())
