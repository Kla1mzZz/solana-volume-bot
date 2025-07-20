import asyncio
from pumpswap_sdk import PumpSwapSDK

from utils.styles import console

from database import get_token_address


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
            console.print(f'[bold red]{err}:[/] ждем {wait_time} сек...')
            await asyncio.sleep(wait_time)


async def get_token_price():
    token_price = await with_retries(sdk.get_token_price, await get_token_address())
    console.print(f'[bold green]Token Price:[/] [bold yellow]{token_price}[/]')


async def buy_token(sol_amount: float, wallet_private_key: str):
    result = await with_retries(sdk.buy, await get_token_address(), sol_amount, wallet_private_key)
    if result.get('status', False):
        console.print(
            f'[bold green] Покупка: {result["message"]}, Hash: {result["data"]["tx_id"]}[/]'
        )
        return True
    else:
        console.print(f'[bold red] Ошибка при покупке: {result["message"]}[/]')
        return False


async def sell_token(amount: float, wallet_private_key: str):
    result = await with_retries(sdk.sell, await get_token_address(), amount, wallet_private_key)
    if result.get('status', False):
        console.print(
            f'[bold green] Продажа: {result["message"]}, Hash: {result["data"]["tx_id"]}[/]'
        )
        return True
    else:
        console.print(f'[bold red] Ошибка при продаже: {result["message"]}[/]')
        return False
