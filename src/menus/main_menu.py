from enum import Enum
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

from menus.base_menu import BaseMenu
from menus.wallet_menu import WalletMenu
from menus.trading_menu import TradingMenu
from utils.styles import console
from utils.decorators import show_message


class MainMenuChoice(Enum):
    CREATE_WALLET = '1'
    TRADING = '2'


class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__('Главное меню')
        self.setup_choices()

    def setup_choices(self):
        self.add_choice(
            MainMenuChoice.CREATE_WALLET.value,
            'Кошельки',
            self.handle_create_wallet,
        )
        self.add_choice(MainMenuChoice.TRADING.value, 'Накрутка', self.handle_trading)

    def handle_create_wallet(self):
        wallet_menu = WalletMenu()
        wallet_menu.display()
        return True

    def handle_trading(self):
        trading_menu = TradingMenu()
        trading_menu.display()
        return True
