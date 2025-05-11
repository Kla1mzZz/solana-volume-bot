from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

from menus.base_menu import BaseMenu
from utils.decorators import show_message

console = Console()


class WalletMenuChoice(Enum):
    CREATE_ONE_WALLET = '1'
    CREATE_MULTIPLE_WALLETS = '2'
    BACK = '9'


class WalletMenu(BaseMenu):
    def __init__(self):
        super().__init__('Меню кошелька')
        self.setup_choices()

    def setup_choices(self):
        self.add_choice(
            WalletMenuChoice.CREATE_ONE_WALLET.value,
            'Создать новый кошелек',
            self.handle_create_new,
        )
        self.add_choice(
            WalletMenuChoice.CREATE_MULTIPLE_WALLETS.value,
            'Создать несколько кошельков',
            self.handle_create_multiple,
        )
        self.add_choice(WalletMenuChoice.BACK.value, 'Назад', self.handle_back)

    @show_message('Создание нового кошелька...')
    def handle_create_new(self):
        self.display()
        return False

    @show_message('Создание нескольких кошельков..')
    def handle_create_multiple(self):
        self.display()
        return False

    def handle_back(self):
        return True
