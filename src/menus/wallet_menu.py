from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

from menus.base_menu import BaseMenu
from utils.decorators import show_message

from service.wallet_service import create_wallet

console = Console()


class WalletMenuChoice(Enum):
    CREATE_MULTIPLE_WALLETS = '1'
    MAIN_WALLET = '2'
    WALLETS_LIST = '3'
    BACK = '9'


class WalletMenu(BaseMenu):
    def __init__(self):
        super().__init__('Кошельки')
        self.setup_choices()

    def setup_choices(self):
        self.add_choice(
            WalletMenuChoice.CREATE_MULTIPLE_WALLETS.value,
            'Создать кошельки',
            self.handle_create_multiple,
        )
        self.add_choice(
            WalletMenuChoice.MAIN_WALLET.value,
            'Основной кошелек',
            self.main_wallet,
        )
        self.add_choice(
            WalletMenuChoice.WALLETS_LIST.value, 'Список кошельков', self.list_wallets
        )
        self.add_choice(WalletMenuChoice.BACK.value, 'Назад', self.handle_back)

    @show_message('Создание нескольких кошельков..')
    async def handle_create_multiple(self):
        self.display()
        wallets = create_wallet(10)
        return False

    def main_wallet(self):
        self.display()
        return False

    def list_wallets(self):
        self.display()
        return False

    def handle_back(self):
        return True
