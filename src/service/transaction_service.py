import asyncio
from pumpswap_sdk import PumpSwapSDK
from solders.keypair import Keypair

from utils.styles import console
from config import settings


sdk = PumpSwapSDK()


async def with_retries(fn, *args, retries=3, delay=2, **kwargs):
    for i in range(retries):
        print(f'{i + 1}/{retries}...')

        f = await fn(*args, **kwargs)
        if type(f) == float:
            return f
        err = f.get('error', None)
        if not err:
            await asyncio.sleep(delay)
            return f
        else:
            wait_time = delay * (i + 1)
            console.print(
                f'[bold red]{err}:[/] ждем {wait_time} сек...'
            )
            await asyncio.sleep(wait_time)


async def get_token_price():
    token_price = await with_retries(sdk.get_token_price, settings.mint)
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


async def buy_token(sol_amount: float, wallet_private_key: str):
    result = await with_retries(sdk.buy, settings.mint, sol_amount, wallet_private_key)
    if result.get('status', False):
        console.print(f'[bold green] Покупка: {result['message']}, Hash: {result['data']['tx_id']}[/]')
        return True
    else:
        console.print(f'[bold red] Ошибка при покупке: {result['message']}[/]')
        return False
    
    return result


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


async def sell_token(amount: float, wallet_private_key: str):
    result = await with_retries(sdk.sell, settings.mint, amount, wallet_private_key)
    if result.get('status', False):
        console.print(f'[bold green] Продажа: {result['message']}, Hash: {result['data']['tx_id']}[/]')
        return True
    else:
        console.print(f'[bold red] Ошибка при продаже: {result['message']}[/]')
        return False