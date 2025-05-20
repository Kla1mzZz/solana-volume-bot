import base58
import asyncio
from pumpswap_sdk import PumpSwapSDK
from solders.keypair import Keypair

from database import get_wallets
from utils.styles import console


sdk = PumpSwapSDK()

mint = 'Dz2dRW6dSFTb7yYXSGrxg1f57KsxeVTLWvom2h3oJJL1'


async def get_token_price():
    token_price = await sdk.get_token_price(mint)
    console.print(f'[bold green]Token Price:[/] [bold yellow]{token_price}[/]')


async def buy_tokens(sol_amount: float):
    wallets = await get_wallets()
    for wallet in wallets:
        await asyncio.sleep(0.2)
        private_key = Keypair().from_bytes(base58.b58decode(wallet.private_key))
        user_private_key = str(private_key)
        result = await sdk.buy(mint, sol_amount, user_private_key)
        print(result)


async def sell_token(amount: float):
    wallets = await get_wallets()
    for wallet in wallets:
        private_key = Keypair().from_bytes(base58.b58decode(wallet.private_key))
        user_private_key = str(private_key)
        result = await sdk.sell(mint, amount, user_private_key)
        print(result)
