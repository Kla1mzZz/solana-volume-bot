from enum import Enum
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

from menus.base_menu import BaseMenu
from menus.wallet_menu import WalletMenu
from utils.styles import console
from utils.decorators import show_message

from service.transaction_service import buy_tokens, sell_token, get_token_price


class TradingMenuChoice(Enum):
    TRADING = '1'
    WITHDRAW = '2'
    TOKEN_PRICE = '3'
    BACK = '9'


class TradingMenu(BaseMenu):
    def __init__(self):
        super().__init__('Накрутка')
        self.setup_choices()

    def setup_choices(self):
        self.add_choice(
            TradingMenuChoice.TRADING.value,
            'Начать накрутку',
            self.making_trade,
        )
        self.add_choice(
            TradingMenuChoice.WITHDRAW.value, 'Вывод средств', self.withdraw_funds
        )
        self.add_choice(
            TradingMenuChoice.TOKEN_PRICE.value, 'Получить цену токена', self.get_main_token_price
        )
        self.add_choice(
            '4', 'Купить токен', self.buy
        )
        self.add_choice(TradingMenuChoice.BACK.value, 'Назад', self.handle_back)

    async def making_trade(self):
        await self.display()
        return True

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
        
    async def buy(self):
        await buy_tokens(1)
        await self.display()
        console.clear()
        

    async def handle_back(self):
        return True
