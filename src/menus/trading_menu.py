from enum import Enum
import random
import keyboard

from rich.prompt import Prompt
from rich.panel import Panel

from solders.pubkey import Pubkey

from menus.base_menu import BaseMenu
from utils.styles import console

from database import get_all_wallets, add_token_to_db, get_token_address
from service.transaction_service import buy_token, sell_token, get_token_price
from service.wallet_service import get_balance, get_token_balance
from config import settings


class TradingMenuChoice(Enum):
    ADD_TOKEN = '1'
    TRADING = '2'
    WITHDRAW = '3'
    TOKEN_PRICE = '4'
    BACK = '9'


class TradingMenu(BaseMenu):
    def __init__(self):
        super().__init__('Накрутка')
        self.setup_choices()

    def setup_choices(self):
        self.add_choice(
            TradingMenuChoice.ADD_TOKEN.value,
            'Добавить токен',
            self.add_token,
        )
        self.add_choice(
            TradingMenuChoice.TRADING.value,
            'Начать накрутку',
            self.making_trade,
        )
        self.add_choice(
            TradingMenuChoice.WITHDRAW.value, 'Вывод средств', self.withdraw_funds
        )
        self.add_choice(
            TradingMenuChoice.TOKEN_PRICE.value,
            'Получить цену токена',
            self.get_main_token_price,
        )
        self.add_choice(TradingMenuChoice.BACK.value, 'Назад', self.handle_back)
        
    async def add_token(self):
        console.print(
            Panel.fit(
                f'[bold italic yellow]{await get_token_address()}[/]',
                subtitle=self.title,
                subtitle_align='left',
                border_style='magenta',
            ),
        )
        choice = Prompt.ask(
            '[bold yellow]Введите адрес токена[/]',
            show_choices=False,
        )
        
        msg = await add_token_to_db(choice)
        console.print(f'[bold green]{msg}[/]')
        await self.display()
        console.clear()

    async def making_trade(self):
        console.print('Нажми "q" чтобы остановить')

        while True:
            try:
                wallets = await get_all_wallets()

                for wallet in wallets[1:]:
                    buy_or_sell = random.choice(['buy', 'sell'])
                    sol_balance = await get_balance(wallet.private_key) / 1_000_000_000
                    mint_balance = await get_token_balance(
                        Pubkey.from_string(wallet.address),
                        Pubkey.from_string(settings.mint),
                    )

                    if buy_or_sell == 'buy':
                        if sol_balance < 0.0015:
                            console.print(f'[bold red]SOL закончились[/]')
                            continue

                        amount_sol = round(random.uniform(0.002, sol_balance), 9)

                        buy_t = await buy_token(amount_sol, wallet.private_key)
                        if not buy_t:
                            console.print(f'[bold red]На балансе мало SOL[/]')
                            continue
                        console.print(f'[bold green]Куплено: на {amount_sol} SOL[/]')
                    elif buy_or_sell == 'sell':
                        if mint_balance < 0.0015:
                            amount_sol = round(random.uniform(0.002, sol_balance), 9)
                            buy_t = await buy_token(amount_sol, wallet.private_key)

                            if not buy_t:
                                console.print(f'[bold red]На балансе мало SOL[/]')
                                continue
                            console.print(f'[bold green]Куплено: на {amount_sol} SOL[/]')
                            continue

                        amount_mint = round(random.uniform(100, mint_balance), 9)
                        await sell_token(amount_mint, wallet.private_key)
                        console.print(f'[bold green]Продано: {amount_mint} токенов[/]')

                if keyboard.is_pressed('q'):
                    console.print('Выход по нажатию "q"')
                    break
            except Exception as e:
                pass

    async def withdraw_funds(self):
        await self.display()
        return True

    async def get_main_token_price(self):
        try:
            await get_token_price()
        except Exception as e:
            console.print('[bold red]Токен не найден[/]: ', e)
        await self.display()
        console.clear()

    async def handle_back(self):
        console.clear()
        console.clear()
        return True
