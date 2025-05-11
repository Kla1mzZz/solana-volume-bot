from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {'success': 'green', 'error': 'red', 'warning': 'yellow', 'info': 'blue'}
)

console = Console(theme=custom_theme)
