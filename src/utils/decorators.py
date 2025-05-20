import time

from rich.console import Console
from rich.panel import Panel
from rich.console import Console


console = Console()


def show_message(
    message: str,
    color: str = 'yellow',
    border_color: str = 'green',
    justify: str = 'center',
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            console.print(
                Panel.fit(
                    f'[{color}]{message}[/]',
                    border_style=border_color,
                    padding=(1, 4),
                ),
                justify=justify,  # type: ignore
            )

            time.sleep(1.5)

            return func(*args, **kwargs)

        return wrapper

    return decorator
