from enum import Enum

from menus.base_menu import BaseMenu
from menus.wallet_menu import WalletMenu
from menus.trading_menu import TradingMenu
from utils.styles import console

class MainMenuChoice(Enum):
    CREATE_WALLET = '1'
    TRADING = '2'


class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__('Главное меню')
        self.setup_choices()

    def setup_choices(self):
        console.clear()
        self.add_choice(
            MainMenuChoice.CREATE_WALLET.value,
            'Кошельки',
            self.handle_create_wallet,
        )
        self.add_choice(MainMenuChoice.TRADING.value, 'Накрутка', self.handle_trading)

    async def handle_create_wallet(self):
        wallet_menu = WalletMenu()
        console.clear()
        await wallet_menu.display()
        return True

    async def handle_trading(self):
        trading_menu = TradingMenu()
        console.clear()
        await trading_menu.display()
        return True
