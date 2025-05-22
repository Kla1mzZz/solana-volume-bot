import asyncio
from menus.main_menu import MainMenu
from database import db_manager


async def main():
    await db_manager.init_db()
    while True:
        menu = MainMenu()

        while True:
            should_exit = await menu.display()
            if should_exit:
                break


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback

        print('❌ Произошла ошибка:')
        traceback.print_exc()
        input('\nНажмите Enter, чтобы закрыть...')
