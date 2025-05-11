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


class MainMenuChoice(Enum):
    CREATE_WALLET = '1'
    SEND_TRANSACTION = '2'


class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__('Главное меню')
        self.setup_choices()

    def setup_choices(self):
        self.add_choice(
            MainMenuChoice.CREATE_WALLET.value,
            'Создать кошелек',
            self.handle_create_wallet,
        )
        self.add_choice(
            MainMenuChoice.SEND_TRANSACTION.value,
            'Отправить транзакцию',
            self.handle_send_transaction,
        )

    def handle_create_wallet(self):
        wallet_menu = WalletMenu()
        wallet_menu.display()
        pass

    @show_message('Отправка транзакции...', border_color='magenta', justify='left')
    def handle_send_transaction(self):
        time.sleep(5)

    @show_message('Выход...')
    def handle_exit(self):
        return True
