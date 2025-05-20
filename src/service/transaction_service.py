import base58
import asyncio
from pumpswap_sdk import PumpSwapSDK
from solders.keypair import Keypair
import httpx
import random

from database import get_wallets
from utils.styles import console


sdk = PumpSwapSDK()

mint = 'Dz2dRW6dSFTb7yYXSGrxg1f57KsxeVTLWvom2h3oJJL1'



async def with_retries(fn, *args, retries=3, delay=2, **kwargs):
    for i in range(retries):
        try:
            return await fn(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait_time = delay * (i + 1)
                console.print(f"[bold red]429 Too Many Requests:[/] чекаємо {wait_time} сек...")
                await asyncio.sleep(wait_time)
            else:
                raise
    raise Exception("❌ Перевищено ліміт повторів після 429")


async def get_token_price():
    token_price = await with_retries(sdk.get_token_price, mint)
    console.print(f'[bold green]Token Price:[/] [bold yellow]{token_price}[/]')


# async def buy_tokens(sol_amount: float):
#     wallets = await get_wallets()
#     for wallet in wallets:
#         await asyncio.sleep(random.uniform(0.3, 0.8))  # 🕒 Рандомна затримка
#         try:
#             private_key = Keypair.from_bytes(base58.b58decode(wallet.private_key))
#             user_private_key = str(private_key)
#             result = await with_retries(sdk.buy, mint, sol_amount, user_private_key)
#             print(result)
#         except Exception as e:
#             console.print(f"[bold red]Помилка при купівлі:[/] {e}")
            
async def buy_tokens(sol_amount: float):
    user_private_key = 'Yop4Jwo1tjhsrbfnjk6fsSmQsauTnViNjr8PqEhdTC8UN99XgvSRbKLAFGqyn4fanpH7HmaTLzwhkQSnS98DsJE'
    result = await with_retries(sdk.buy, mint, sol_amount, user_private_key)
    print(result)


# async def sell_tokens(amount: float):
#     wallets = await get_wallets()
#     for wallet in wallets:
#         await asyncio.sleep(random.uniform(0.3, 0.8))
#         try:
#             private_key = Keypair.from_bytes(base58.b58decode(wallet.private_key))
#             user_private_key = str(private_key)
#             result = await with_retries(sdk.sell, mint, amount, user_private_key)
#             print(result)
#         except Exception as e:
#             console.print(f"[bold red]Помилка при продажу:[/] {e}")
            
            
async def sell_tokens(amount: float):
    user_private_key = 'Yop4Jwo1tjhsrbfnjk6fsSmQsauTnViNjr8PqEhdTC8UN99XgvSRbKLAFGqyn4fanpH7HmaTLzwhkQSnS98DsJE'
    result = await sdk.sell(mint, amount, user_private_key)
    print(result)
