from typing import Callable
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

from utils.styles import console


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
        self.choices: list[tuple[str, str, Callable]] = []

    def add_choice(self, num: str, choice: str, handler: Callable):
        """
        Добавляет пункт в меню.

        Args:
            num (str): Номер пункта меню (строка).
            choice (str): Описание пункта меню.
            handler (Callable): Функция, которая будет вызвана при выборе этого пункта.
        """
        self.choices.append((num, choice, handler))

    def display(self):
        """
        Отображает меню в консоли, ожидает ввод пользователя и вызывает соответствующий обработчик.

        Выводится панель с заголовком и таблица с пунктами меню. Пользователь может выбрать пункт по номеру.
        Если выбран пункт '0', программа завершает выполнение.
        """
        console.clear()

        console.print(
            Panel.fit(
                '[bold italic yellow]Solana Volume Bot[/]',
                subtitle=self.title,
                subtitle_align='left',
                border_style='magenta',
                padding=(1, 2),
            )
        )

        menu_table = Table(show_header=False, box=box.ROUNDED, border_style='magenta')

        for num, choice, _ in self.choices:
            menu_table.add_row(f'[bold cyan]{num}.[/]', f'[bold cyan]{choice}[/]')

        menu_table.add_row('[bold red]0.[/]', '[bold red]Выход[/]')
        console.print(menu_table, justify='center')

        choice = Prompt.ask(
            '[bold yellow]Выберите пункт меню[/]',
            choices=[choice[0] for choice in self.choices] + ['0'],
            show_choices=False,
        )

        for num, _, handle in self.choices:
            if choice == '0':
                exit()

            if choice == num:
                return handle()
