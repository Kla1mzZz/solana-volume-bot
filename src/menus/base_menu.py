from typing import Callable
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.columns import Columns

from utils.styles import console
from database import get_wallets, get_main_wallet, add_wallets_to_db
from service.wallet_service import create_wallet

import inspect


class BaseMenu:
    """
    Базовый класс для создания текстового меню в консоли с использованием библиотеки rich.

    Атрибуты:
        title (str): Заголовок меню, отображаемый в панели.
        choices (list[tuple[str, str, Callable]]): Список пунктов меню, каждый из которых представлен кортежем
            (номер пункта, текстовое описание, функция-обработчик).
    """

    def __init__(self, title: str):
        """
        Инициализирует объект BaseMenu с заголовком меню.

        Args:
            title (str): Заголовок, который будет отображаться в меню.
        """
        self.title = title
        self.wallet_address = ''
        self.wallet_secret_key = ''
        self.choices: list[tuple[str, str, Callable]] = []

    async def init_wallet(self):
        wallets = await get_wallets()

        if not wallets:
            wallet = await create_wallet()
            await add_wallets_to_db(wallet)
            main_wallet = await get_main_wallet()
        else:
            main_wallet = await get_main_wallet()
            self.wallet_address = main_wallet.address
            self.wallet_secret_key = main_wallet.private_key

        self.wallet_address = main_wallet.address
        self.wallet_secret_key = main_wallet.private_key

    def add_choice(self, num: str, choice: str, handler: Callable):
        """
        Добавляет пункт в меню.

        Args:
            num (str): Номер пункта меню (строка).
            choice (str): Описание пункта меню.
            handler (Callable): Функция, которая будет вызвана при выборе этого пункта.
        """
        self.choices.append((num, choice, handler))

    async def display(self):
        """
        Отображает меню в консоли, ожидает ввод пользователя и вызывает соответствующий обработчик.

        Выводится панель с заголовком и таблица с пунктами меню. Пользователь может выбрать пункт по номеру.
        Если выбран пункт '0', программа завершает выполнение.
        """
        await self.init_wallet()

        console.print(
            Panel.fit(
                '[bold italic yellow]Solana Volume Bot[/]',
                subtitle=self.title,
                subtitle_align='left',
                border_style='magenta',
            ),
        )

        console.print(
            Panel.fit(
                f'Адрес:[bold italic yellow] {self.wallet_address}[/]\n\nПриватный ключ: [bold italic yellow]{self.wallet_secret_key}[/]',
                title='Основной кошелек',
                border_style='magenta',
                width=80,
            ),
            justify='center',
        )

        menu_table = Table(
            show_header=False, box=box.ROUNDED, border_style='magenta', padding=(0, 3)
        )

        for num, choice, _ in self.choices:
            menu_table.add_row(f'[bold cyan]{num}.[/]', f'[bold cyan]{choice}[/]')

        menu_table.add_row('[bold red]0.[/]', '[bold red]Выход[/]')
        console.print(menu_table, justify='center')

        choice = Prompt.ask(
            '[bold yellow]Выберите пункт меню[/]',
            choices=[choice[0] for choice in self.choices] + ['0'],
            show_choices=False,
        )

        if choice == '0':
            exit()
        
        for num, _, handle in self.choices:
            if choice == num:
                result = handle()
                if inspect.isawaitable(result):
                    return await result
                return result
