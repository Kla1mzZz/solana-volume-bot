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


class TradingMenuChoice(Enum):
    TRADING = '1'
    WITHDRAW = '2'
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
        self.add_choice(TradingMenuChoice.BACK.value, 'Назад', self.handle_back)

    async def making_trade(self):
        await self.display()
        return True

    async def withdraw_funds(self):
        await self.display()
        return True

    def handle_back(self):
        return True
