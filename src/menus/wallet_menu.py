import time
from enum import Enum

from rich.console import Console
from rich.table import Table, Column
from rich import box
from rich.prompt import Prompt

from solders.pubkey import Pubkey

from menus.base_menu import BaseMenu
from utils.decorators import show_message

from service.wallet_service import (
    create_wallet,
    money_distribution,
    get_balance,
    money_withdrawal,
    get_token_balance,
)
from database import get_main_wallet, add_wallets_to_db, get_all_wallets, get_token_address

console = Console()


class WalletMenuChoice(Enum):
    CREATE_MULTIPLE_WALLETS = '1'
    WALLETS_LIST = '2'
    MONEY_TO_WALLETS = '3'
    MONEY_WITHDRAW = '4'
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
            WalletMenuChoice.WALLETS_LIST.value, 'Список кошельков', self.list_wallets
        )
        self.add_choice(
            WalletMenuChoice.MONEY_TO_WALLETS.value,
            'Распределить деньги',
            self.money_to_wallets,
        )
        self.add_choice(
            WalletMenuChoice.MONEY_WITHDRAW.value, 'Вывод средств', self.withdraw_funds
        )
        self.add_choice(WalletMenuChoice.BACK.value, 'Назад', self.handle_back)

    async def handle_create_multiple(self):
        choice = Prompt.ask(
            '[bold yellow]Введите количество кошельков[/]',
            show_choices=False,
        )

        wallets = await create_wallet(int(choice))
        await add_wallets_to_db(wallets)
        for n, wallet in enumerate(wallets):
            time.sleep(0.01)
            console.print(f'{n + 1}. Кошелек создан: [green] {wallet[0]}[/]')

        console.print('[bold green]Кошельки созданы[/]')
        time.sleep(2)
        await self.display()
        console.clear()

    async def main_wallet(self):
        main_wallet = await get_main_wallet()
        console.print(f'Основной кошелек: [green]{main_wallet.address}[/]')

    @show_message('Загрузка кошельков')
    async def list_wallets(self):
        wallets = await get_all_wallets()

        table = Table(
            Column('id', style='bold cyan'),
            Column('Адрес', style='bold yellow', overflow='fold'),
            Column('Приватный ключ', style='bold yellow', overflow='fold'),
            Column('Баланс SOL', style='bold yellow', overflow='fold'),
            Column('Баланс MINT', style='bold yellow', overflow='fold'),
            box=box.ROUNDED,
            title='Список кошельков',
            title_style='bold yellow',
            border_style='magenta',
        )
        for wallet in wallets:
            mint = Pubkey.from_string(await get_token_address())
            wall = Pubkey.from_string(wallet.address)
            sol_balance = await get_balance(wallet.private_key) / 1_000_000_000
            mint_balance = await get_token_balance(wall, mint)

            table.add_row(
                str(wallet.id),
                wallet.address,
                f'{wallet.private_key}\n',
                str(sol_balance),
                str(mint_balance),
            )

        console.print(table)

        await self.display()
        console.clear()

    async def money_to_wallets(self):
        choice = Prompt.ask(
            '[bold yellow]Введите сумму в SOL[/]',
            show_choices=False,
        )
        if float(choice) < 0.0015:
            console.print('[bold red]Сумма должна быть больше 0.0015[/]')
            await self.display()
            return
        await money_distribution(float(choice))

        time.sleep(2)
        await self.display()
        console.clear()

    async def withdraw_funds(self):
        await money_withdrawal()

        time.sleep(2)
        await self.display()
        console.clear()

    async def handle_back(self):
        console.clear()
        console.clear()
        return True
