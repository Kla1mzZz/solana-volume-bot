import base58
import asyncio
from pumpswap_sdk import PumpSwapSDK
from solders.keypair import Keypair
import random

from database import get_wallets
from service.wallet_service import get_balance
from utils.styles import console


sdk = PumpSwapSDK()

mint = 'Dz2dRW6dSFTb7yYXSGrxg1f57KsxeVTLWvom2h3oJJL1'



async def with_retries(fn, *args, retries=3, delay=2, **kwargs):
    for i in range(retries):
        print(f"Retry {i + 1}/{retries}...")

        f = await fn(*args, **kwargs)
        err = f.get('error', None)
        if not err:
            await asyncio.sleep(delay)
            return f
        else:
            wait_time = delay * (i + 1)
            console.print(f"[bold red]429 Too Many Requests:[/] чекаємо {wait_time} сек...")
            await asyncio.sleep(wait_time)


async def get_token_price():
    token_price = await with_retries(sdk.get_token_price, mint)
    console.print(f'[bold green]Token Price:[/] [bold yellow]{token_price}[/]')


# async def buy_tokens():
#     wallets = await get_wallets()
#     for wallet in wallets:
#         await asyncio.sleep(random.uniform(0.3, 1))  # 🕒 Рандомна затримка
#         try:
#             private_key = Keypair.from_bytes(base58.b58decode(wallet.private_key))
#             wallet_balance = await get_balance(wallet.private_key)
#             sol_amount = wallet_balance / 1_000_000_000
#             user_private_key = str(private_key)
#             result = await with_retries(sdk.buy, mint, sol_amount, user_private_key)
            
#             print(result)
#         except Exception as e:
#             console.print(f"[bold red]Помилка при купівлі:[/] {e}")
            
async def buy_tokens(sol_amount: float):
    user_private_key = 'Yop4Jwo1tjhsrbfnjk6fsSmQsauTnViNjr8PqEhdTC8UN99XgvSRbKLAFGqyn4fanpH7HmaTLzwhkQSnS98DsJE'
    result = await with_retries(sdk.buy, mint, sol_amount, user_private_key)
    console.print(f'[bold green] Покупка: {result}[/]')


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
    result = await with_retries(sdk.sell, mint, amount, user_private_key)
    console.print(f'[bold green] Продажа: {result}[/]')
