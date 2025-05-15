import asyncio
from menus.main_menu import MainMenu


async def main():
    while True:
        menu = MainMenu()

        while True:
            should_exit = await menu.display()
            if should_exit:
                break


if __name__ == '__main__':
    asyncio.run(main())
